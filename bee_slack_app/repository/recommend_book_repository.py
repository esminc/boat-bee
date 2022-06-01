import json
from typing import Optional


class RecommendBookRepository:  # pylint: disable=too-few-public-methods
    recommend_info = None

    def __init__(self) -> None:
        self.recommend_info = self._load_recommend_info()

    def fetch(self, user_id: str) -> Optional[dict[str, str]]:
        """
        おすすめの本を取得する

        Args:
            user_id : ユーザID
        Returns:
           MLモデルとおすすめの本のISBNを辞書形式で返す
        """

        return self.recommend_info["result"].get(user_id)

    def created_at(self) -> str:
        """
        おすすめ情報が生成されたタイムスタンプを取得する

        Returns:
           生成されたタイムスタンプをISO 8601形式で返す
        """

        return self.recommend_info["metadata"]["created_at"]

    def _load_recommend_info(self):
        with open(
            "./ml/models/recommended_book.json", encoding="utf-8", mode="r"
        ) as json_file:
            return json.load(json_file)
