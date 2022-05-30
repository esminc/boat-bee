"""興味ありのおすすめ本を追加・更新します
"""
import os
from typing import Optional

from bee_slack_app.model.suggested_book import SuggestedBook
from bee_slack_app.repository.database import get_database_client


class SuggestedBookRepository:
    def __init__(self):
        self.table = get_database_client().Table(
            os.environ["DYNAMODB_TABLE"] + "-suggested-book"
        )

    def get(self, user_id: str, isbn: str, ml_model: str) -> Optional[SuggestedBook]:
        """
        自分が興味ありとした本を取得する

        Args:
            user_id : 検索する、興味あり情報のuser_id
            isbn    : 検索する、興味あり情報のisbn
            ml_model: 検索する、興味あり情報のml_model

        Returns:
            SuggestedBook: 取得した、興味ありとした本の情報。未登録の場合は、Noneを返します。
        """
        response = self.table.get_item(
            Key={
                "user_id": user_id,
                "suggested_book_sk": isbn + "#" + ml_model,
            }
        )
        item = response.get("Item")
        if item is None:
            return item

        suggested_book_sk = item["suggested_book_sk"].split("#")
        suggested_book: SuggestedBook = {
            "user_id": item["user_id"],
            "isbn": suggested_book_sk[0],
            "ml_model": suggested_book_sk[1],
            "interested": item["interested"],
            "updated_at": item["updated_at"],
        }
        return suggested_book
