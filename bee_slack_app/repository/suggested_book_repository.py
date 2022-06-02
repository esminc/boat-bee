"""おすすめされた本を、追加・更新します
"""
import os
from typing import Optional

from bee_slack_app.model.suggested_book import SuggestedBook
from bee_slack_app.repository.database import get_database_client


# DBソートキーの生成
def encode_sort_key(isbn: str, ml_model: str) -> str:
    return isbn + "#" + ml_model


# DBソートキーの分解
def decode_sort_key(sort_key: str) -> tuple[str, str]:
    # sort keyにはisbnとml_model情報が#で連結されて入っている
    items = sort_key.split("#")
    isbn = items[0]
    ml_model = items[1]
    return (isbn, ml_model)


class SuggestedBookRepository:
    def __init__(self):
        self.table = get_database_client().Table(
            os.environ["DYNAMODB_TABLE"] + "-suggested-book"
        )

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
        response = self.table.get_item(
            Key={
                "user_id": user_id,
                "suggested_book_sk": encode_sort_key(isbn, ml_model),
            }
        )
        item = response.get("Item")
        if item is None:
            return None

        isbn, ml_model = decode_sort_key(item["suggested_book_sk"])
        suggested_book: SuggestedBook = {
            "user_id": item["user_id"],
            "isbn": isbn,
            "ml_model": ml_model,
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
            "suggested_book_sk": encode_sort_key(
                suggested_book["isbn"], suggested_book["ml_model"]
            ),
            "interested": suggested_book["interested"],
            "updated_at": suggested_book["updated_at"],
        }

        self.table.put_item(Item=item)
