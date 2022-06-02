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

        return (
            self.recommend_info["result"].get(user_id)
            if self.recommend_info is not None
            else None
        )

    def fetch_metadata(self) -> Optional[dict]:
        """
        おすすめ情報のメタデータを取得する
        メタデータの内容はアプリの都合により変動があると思われるため
        リポジトリでは辞書形式の読み出しに留めて柔軟性を確保しておく
        辞書の内容については上位側で取り出す

        Returns:
           JSONファイルに格納されているメタデータを辞書形式で返す
        """

        return (
            self.recommend_info["metadata"] if self.recommend_info is not None else None
        )

    @staticmethod
    def _load_recommend_info():
        with open(
            "./ml/models/recommended_book.json", encoding="utf-8", mode="r"
        ) as json_file:
            return json.load(json_file)
