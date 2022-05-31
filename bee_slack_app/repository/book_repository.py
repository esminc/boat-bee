import os
from typing import Optional, TypedDict

import boto3  # type: ignore

from bee_slack_app.model.book import Book
from bee_slack_app.repository.database import get_database_client
from bee_slack_app.utils import datetime

BOOK_TABLE_PK = "book_pk"
BOOK_TABLE_PK_VALUE = "book_pk_value"
BOOL_UPDATED_AT_GSI = "updatedAtIndex"


class BookItemKey(TypedDict):
    isbn: str


class GetResponse(TypedDict):
    items: list[Book]
    last_key: Optional[BookItemKey]


class BookRepository:
    class GetConditions(TypedDict):
        score_for_me: Optional[str]
        score_for_others: Optional[str]

    def __init__(self):
        self.table = get_database_client().Table(os.environ["DYNAMODB_TABLE"] + "-book")

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
            BOOK_TABLE_PK: BOOK_TABLE_PK_VALUE,
            "isbn": book["isbn"],
            "title": book["title"],
            "author": book["author"],
            "url": book["url"],
            "image_url": book["image_url"],
            "updated_at": updated_at,
        }

        self.table.put_item(Item=item)

    def fetch(
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

        def query(exclusive_start_key=None, max_item_count=None):
            option = {}
            if exclusive_start_key:
                option["ExclusiveStartKey"] = exclusive_start_key
            if max_item_count:
                option["Limit"] = max_item_count

            response = self.table.query(
                IndexName=BOOL_UPDATED_AT_GSI,
                KeyConditionExpression=boto3.dynamodb.conditions.Key(BOOK_TABLE_PK).eq(
                    BOOK_TABLE_PK_VALUE
                ),
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
