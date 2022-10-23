"""おすすめされた本を、追加・更新します
"""
from typing import Optional

from bee_slack_app.model import SuggestedBook
from bee_slack_app.repository import database

GSI_PK_VALUE = "suggested_book"


def _encode_partition_key(*, user_id: str, isbn: str, ml_model: str) -> str:
    return f"suggested_book#{user_id}#{isbn}#{ml_model}"


class SuggestedBookRepository:
    def __init__(self):
        self.table = database.get_table()

    def get(self, *, user_id: str, isbn: str, ml_model: str) -> Optional[SuggestedBook]:
        """
        おすすめされた本を取得する

        Args:
            user_id : おすすめされたユーザのuser_id
            isbn    : おすすめされた本のisbn
            ml_model: おすすめされた本のml_model

        Returns:
            SuggestedBook: おすすめされた本の情報を返す。未登録の場合は、Noneを返します。
        """
        return self.table.get_item(
            Key={
                database.PK: _encode_partition_key(
                    user_id=user_id, isbn=isbn, ml_model=ml_model
                ),
            }
        ).get("Item")

    def create(self, suggested_book: SuggestedBook) -> None:
        """
        データを追加および上書きします
        """
        partition_key = _encode_partition_key(
            user_id=suggested_book["user_id"],
            isbn=suggested_book["isbn"],
            ml_model=suggested_book["ml_model"],
        )

        item = {
            database.PK: partition_key,
            database.GSI_PK: GSI_PK_VALUE,
            database.GSI_0_SK: suggested_book["user_id"],
            database.GSI_1_SK: suggested_book["isbn"],
            database.GSI_2_SK: suggested_book["ml_model"],
            "user_id": suggested_book["user_id"],
            "isbn": suggested_book["isbn"],
            "ml_model": suggested_book["ml_model"],
            "interested": suggested_book["interested"],
            "updated_at": suggested_book["updated_at"],
        }

        self.table.put_item(Item=item)
