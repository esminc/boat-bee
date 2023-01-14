from typing import Union

import numpy as np
import pandas as pd
from gensim.models.word2vec import Word2Vec

from .nlp.wakati import parse_to_words
from .types import Review, SuggestedBook


class BeeContentsBaseRecommender:
    df_review = None
    df_interested = None

    user_book_matrix = None
    book2index = None
    index2book = None
    word2vec = None

    def __init__(
        self,
        reviews: list[Review],
        suggested_books: list[SuggestedBook],
    ):
        # 必要なプロパティだけを取り出す
        reviews = [
            {
                "user_id": review["user_id"],
                "isbn": review["isbn"],
                "score_for_me": review["score_for_me"],
                "title": review["book_title"],
                "contents": review["book_description"],
            }
            for review in reviews
        ]

        self.df_review = pd.DataFrame(reviews)

        self.user_book_matrix = self.df_review.pivot(
            index="user_id", columns="isbn", values="score_for_me"
        ).fillna(0)

        self.book2index = dict(
            zip(
                self.user_book_matrix.columns, range(len(self.user_book_matrix.columns))
            )
        )
        self.index2book = {v: k for k, v in self.book2index.items()}

        df_suggested_book = [
            {
                "isbn": suggested_book["isbn"],
                "user_id": suggested_book["user_id"],
                "ml_model": suggested_book["ml_model"],
                "interested": suggested_book["interested"],
            }
            for suggested_book in suggested_books
        ]

        df_suggested_book = pd.DataFrame(suggested_books)

        df_suggested_book = df_suggested_book[
            df_suggested_book["interested"] == True
        ].reset_index(drop=True)

        for index, row in self.df_review.iterrows():

            self.df_review.at[index, "contents"] = (
                row["contents"] if len(row["contents"]) > 3 else row["title"]
            )

        self.df_interested = df_suggested_book.dropna()

        self.df_interested["description"] = self.df_interested["isbn"].map(
            lambda isbn: self.df_review[self.df_review["isbn"] == isbn].iloc[0][
                "contents"
            ]
            if len(self.df_review["contents"]) > 3
            else self.df_review[self.df_review["isbn"] == isbn].iloc[0]["title"]
        )

    def train(self):
        self.df_review["words"] = self.df_review["contents"].map(parse_to_words)

        # 単語をベクトル化するためのモデルを作成する
        sentences = []
        for contents in self.df_review["words"]:
            sentences.append(contents)

        self.word2vec = Word2Vec(
            sentences=sentences, sg=1, vector_size=100, min_count=0, window=300
        )

        self.df_review["vector"] = ""

        for i in range(len(self.df_review)):
            vector = np.zeros(100)
            for word in self.df_review.at[i, "words"]:
                vector += self.word2vec.wv[word].tolist()

            self.df_review.at[i, "vector"] = self._normalize(vector)

    def predict(self, user_id: str, samples: int = 1) -> Union[list[str], str]:

        df_review_unique = self.df_review.drop_duplicates(subset="isbn")

        interested_vector = self._interested_vec(user_id)
        sim_list = self._get_similarities(interested_vector, df_review_unique["vector"])
        sim_list = sorted(
            sim_list,
            key=lambda x: x["sim"],
            reverse=True,
        )
        sim_list_isbn = [x["isbn"] for x in sim_list]

        return sim_list_isbn[0] if samples == 1 else sim_list_isbn[:samples]

    @staticmethod
    def _normalize(v):
        return v / np.linalg.norm(v)

    def _interested_vec(self, user_id: str) -> list[float]:
        """
        指定されたユーザが興味ありとした本を平均した特徴ベクトルを計算する

        Args:
            user_id:特徴ベクトルを計算したいユーザID
        Return:
            指定されたユーザが興味ありとした本を平均した特徴ベクトル
        """
        df_interested_of_user = self.df_interested[
            self.df_interested["user_id"] == user_id
        ]
        df_interested_of_user["words"] = df_interested_of_user["description"].map(
            parse_to_words
        )
        sentences = []
        for description in df_interested_of_user["words"]:
            sentences.extend(description)

        vector = np.zeros(100)
        for word in sentences:
            vector += self.word2vec.wv[word].tolist()

        interested_vector = self._normalize(vector)

        return interested_vector

    def _get_similarities(
        self, interested_vector: list[float], vector: list[list[float]]
    ) -> list[dict[str, Union[str, float]]]:
        """
        興味あり本ベクトルとレビュー投稿された本ベクトルのコサイン類似度行列を計算してリストで返す

        Args:
            interested_vector:興味ありの本のベクトル
            vector:レビュー投稿された本のベクトルのリスト
        Return:
            興味ありの本とレビュー投稿されたそれぞれの本とのコサイン類似度のリスト
            形式はISBNとコサイン類似度を持つdictのlistとなる

        """

        sim_list = []
        for i, v in enumerate(vector):
            sim = np.dot(v, interested_vector) / (
                np.linalg.norm(v) * np.linalg.norm(interested_vector)
            )
            isbn = self.index2book[i]

            sim_list.append({"isbn": isbn, "sim": sim})
        return sim_list
