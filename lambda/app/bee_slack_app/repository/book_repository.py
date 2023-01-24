from typing import Optional, Tuple, TypedDict

import boto3  # type: ignore

from bee_slack_app.model import Book
from bee_slack_app.repository import database
from bee_slack_app.utils import datetime

GSI_PK_VALUE = "book"


def _encode_partition_key(*, isbn: str) -> str:
    return f"book#{isbn}"


class BookItemKey(TypedDict):
    isbn: str


class GetResponse(TypedDict):
    items: list[Book]
    last_key: Optional[BookItemKey]


class BookRepository:
    class GetConditions(TypedDict):
        score_for_me: Optional[str]
        score_for_others: Optional[str]

    def __init__(self) -> None:
        self.table = database.get_table()

    def put(self, *, book: Book) -> None:
        """
        レビューが投稿されている本を保存する

        Args:
            book: 保存する本のデータ
        """

        updated_at = str(
            datetime.TIMESTAMP_MAX
            - datetime.iso_format_to_timestamp(book["updated_at"])
        )

        item = {
            database.PK: _encode_partition_key(isbn=book["isbn"]),
            database.GSI_PK: GSI_PK_VALUE,
            database.GSI_0_SK: updated_at,
            "isbn": book["isbn"],
            "title": book["title"],
            "author": book["author"],
            "url": book["url"],
            "image_url": book["image_url"],
            "description": book["description"],
            "updated_at": updated_at,
        }

        self.table.put_item(Item=item)

    def fetch(self, *, isbn: str) -> Optional[Book]:
        """
        レビューが投稿されている本を取得する

        Args:
            isbn: ISBN
        Returns:
            取得した本
        """
        partition_key = _encode_partition_key(isbn=isbn)
        item = self.table.get_item(Key={database.PK: partition_key}).get("Item")

        if not item:
            return None

        item["updated_at"] = datetime.timestamp_to_iso_format(
            datetime.TIMESTAMP_MAX - float(item["updated_at"])
        )

        return item

    def fetch_all(
        self,
        *,
        limit: Optional[int] = None,
        start_key: Optional[BookItemKey] = None,
    ) -> GetResponse:
        """
        レビューが投稿されている本のリストを取得する

        Args:
            limit: 取得するアイテムの上限数
            start_key: 読み込み位置を表すキー
        Returns:
            items: レビュー投稿日時が新しい順にソート済みの、本のリスト
            last_key: 読み込んだ最後のキー
        """
        QueryResult = Tuple[list[Book], Optional[BookItemKey]]

        def query(exclusive_start_key=None, max_item_count=None) -> QueryResult:
            option = {}
            if exclusive_start_key:
                option["ExclusiveStartKey"] = exclusive_start_key
            if max_item_count:
                option["Limit"] = max_item_count

            response = self.table.query(
                IndexName=database.GSI_0,
                KeyConditionExpression=boto3.dynamodb.conditions.Key(
                    database.GSI_PK
                ).eq(GSI_PK_VALUE),
                **option,
            )

            return response["Items"], response.get("LastEvaluatedKey")

        items, last_key = query(
            exclusive_start_key=start_key,
            max_item_count=limit,
        )

        if not limit:
            # レスポンスに LastEvaluatedKey が含まれなくなるまでループ処理を実行する
            # see https://dev.classmethod.jp/articles/hot-to-get-more-than-1mb-of-data-from-dynamodb-when-using-scan/
            while last_key is not None:
                new_items, last_key = query(exclusive_start_key=last_key)
                items.extend(new_items)

        for item in items:

            item["updated_at"] = datetime.timestamp_to_iso_format(
                datetime.TIMESTAMP_MAX - float(item["updated_at"])
            )

        return {"items": items, "last_key": last_key}
