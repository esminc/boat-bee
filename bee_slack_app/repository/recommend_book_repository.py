import json
from typing import Optional


class RecommendBookRepository:  # pylint: disable=too-few-public-methods
    recommend_book_dict = None

    def fetch(self, user_id: str) -> Optional[dict]:
        """
        おすすめの本を取得する

        Args:
            user_id : ユーザID
        Returns:
           MLモデルとおすすめの本のISBNを辞書形式で返す
        """
        if not self.recommend_book_dict:
            self.recommend_book_dict = self._load_recommend_book_dict()

        return self.recommend_book_dict.get(user_id)

    @staticmethod
    def _load_recommend_book_dict():
        with open(
            "./ml/models/recommended_book.json", encoding="utf-8", mode="r"
        ) as json_file:
            return json.load(json_file)
