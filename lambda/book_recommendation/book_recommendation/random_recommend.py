import random
from typing import Union

import pandas as pd

from .types import Review


class BeeRandomRecommender:
    df_review = None

    def __init__(self, reviews: list[Review]):
        # 必要なプロパティだけを取り出す
        reviews = [
            {
                "user_id": review["user_id"],
                "isbn": review["isbn"],
            }
            for review in reviews
        ]

        self.df_review = pd.DataFrame(reviews)

    def train(self):
        pass

    def predict(self, user_id, samples: int = 1) -> Union[list[str], str]:
        """
        指定されたユーザに対するおすすめの本を選ぶ

        Args:
            user_id : おすすめを提示したいユーザ
            samples : おすすめしたいアイテム数（省略時は1個）
        Returns:
            samples == 1の場合:ISBN
            samples != 1の場合:ISBNのリスト
        """

        isbn_set = set(self.df_review["isbn"])

        recommend = random.sample(isbn_set, samples)
        recommend = [str(x) for x in recommend]

        # 1冊の場合はISBN、複数の場合はISBNのリストを返す
        return recommend[0] if samples == 1 else recommend
