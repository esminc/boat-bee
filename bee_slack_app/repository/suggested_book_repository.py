"""おすすめされた本を、追加・更新します
"""
import os

from bee_slack_app.model.suggested_book import SuggestedBook
from bee_slack_app.repository.database import get_database_client


class SuggestedBookRepository:
    def __init__(self):
        self.table = get_database_client().Table(
            os.environ["DYNAMODB_TABLE"] + "-suggested-book"
        )

    def get(self, user_id: str, isbn: str, ml_model: str) -> SuggestedBook:
        """
        おすすめされた本を取得する

        Args:
            user_id : おすすめされたユーザのuser_id
            isbn    : おすすめされた本のisbn
            ml_model: おすすめされた本のml_model

        Returns:
            SuggestedBook: おすすめされた本の情報を返す。未登録の場合は、Noneを返します。
        """
        response = self.table.get_item(
            Key={
                "user_id": user_id,
                "suggested_book_sk": isbn + "#" + ml_model,
            }
        )
        item = response.get("Item")
        if item is None:
            return None

        suggested_book_sk = item["suggested_book_sk"].split("#")
        suggested_book: SuggestedBook = {
            "user_id": item["user_id"],
            "isbn": suggested_book_sk[0],
            "ml_model": suggested_book_sk[1],
            "interested": item["interested"],
            "updated_at": item["updated_at"],
        }
        return suggested_book

    def create(self, suggested_book: SuggestedBook) -> None:
        """
        データを追加および上書きします
        """
        item = {
            "user_id": suggested_book["user_id"],
            "suggested_book_sk": suggested_book["isbn"]
            + "#"
            + suggested_book["ml_model"],
            "interested": suggested_book["interested"],
            "updated_at": suggested_book["updated_at"],
        }

        self.table.put_item(Item=item)
