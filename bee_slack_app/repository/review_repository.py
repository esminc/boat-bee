from typing import Optional, TypedDict

import boto3  # type: ignore
from boto3.dynamodb.conditions import Key  # type: ignore

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.repository import database

GSI_PK_VALUE = "review"


def _encode_partition_key(*, user_id: str, isbn: str) -> str:
    return f"review#{user_id}#{isbn}"


class ReviewItemKey(TypedDict):
    isbn: str


class GetResponse(TypedDict):
    items: list[ReviewContents]
    last_key: Optional[ReviewItemKey]


class ReviewRepository:
    class GetConditions(TypedDict):
        score_for_me: Optional[str]
        score_for_others: Optional[str]

    def __init__(self):
        self.table = database.get_table()

    def get(self, *, user_id: str, isbn: str) -> Optional[ReviewContents]:
        """
        本のレビューを取得する

        Args:
            user_id : レビューのユーザID
            isbn : レビューのISBN
        Returns:
            本のレビュー。存在しない場合はNone。
        """
        partition_key = _encode_partition_key(user_id=user_id, isbn=isbn)
        return self.table.get_item(Key={database.PK: partition_key}).get("Item")

    def get_all(self) -> list[ReviewContents]:
        """
        本のレビューを全て取得する

        Returns: 本のレビューのリスト
        """

        def query(exclusive_start_key=None):
            option = {}
            if exclusive_start_key:
                option["ExclusiveStartKey"] = exclusive_start_key

            response = self.table.query(
                IndexName=database.GSI_0,
                KeyConditionExpression=Key(database.GSI_PK).eq(GSI_PK_VALUE),
            )

            return response["Items"], response.get("LastEvaluatedKey")

        items, last_key = query()

        # レスポンスに LastEvaluatedKey が含まれなくなるまでループ処理を実行する
        # see https://dev.classmethod.jp/articles/hot-to-get-more-than-1mb-of-data-from-dynamodb-when-using-scan/
        while last_key is not None:
            new_items, last_key = query(exclusive_start_key=last_key)
            items.extend(new_items)

        return items

    def get_by_isbn(self, *, isbn: str) -> list[ReviewContents]:
        """
        ISBNから、本のレビューを取得する

        Args:
            isbn : 取得する本のISBN
        Returns:
            レビューのリスト。指定したISBNで見つからない場合は空のリストを返す。
        """
        return self.table.query(
            IndexName=database.GSI_2,
            KeyConditionExpression=Key(database.GSI_PK).eq(GSI_PK_VALUE)
            & Key(database.GSI_2_SK).eq(isbn),
        )["Items"]

    def get_by_user_id(self, *, user_id: str) -> list[ReviewContents]:
        """
        ユーザIDから、本のレビューを取得する

        Args:
            user_id : 取得する本のユーザID
        Returns:
            レビューのリスト。指定したユーザIDで見つからない場合は空のリストを返す。
        """
        return self.table.query(
            IndexName=database.GSI_1,
            KeyConditionExpression=Key(database.GSI_PK).eq(GSI_PK_VALUE)
            & Key(database.GSI_1_SK).eq(user_id),
        )["Items"]

    def fetch(
        self,
        *,
        user_id: str,
        limit: Optional[int] = None,
        start_key: Optional[ReviewItemKey] = None,
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
                IndexName=database.GSI_1,
                KeyConditionExpression=boto3.dynamodb.conditions.Key(
                    database.GSI_PK
                ).eq(GSI_PK_VALUE)
                & Key(database.GSI_1_SK).eq(user_id),
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

        return {"items": items, "last_key": last_key}

    def create(self, review):
        partition_key = _encode_partition_key(
            user_id=review["user_id"], isbn=review["isbn"]
        )

        item = {
            database.PK: partition_key,
            database.GSI_PK: GSI_PK_VALUE,
            database.GSI_0_SK: review["updated_at"],
            database.GSI_1_SK: review["user_id"],
            database.GSI_2_SK: review["isbn"],
            "user_id": review["user_id"],
            "book_title": review["book_title"],
            "isbn": review["isbn"],
            "score_for_me": review["score_for_me"],
            "score_for_others": review["score_for_others"],
            "review_comment": review["review_comment"],
            "updated_at": review["updated_at"],
            "book_image_url": review["book_image_url"],
            "book_author": review["book_author"],
            "book_url": review["book_url"],
            "book_description": review["book_description"],
        }

        self.table.put_item(Item=item)

        return item

    def delete(self):
        # 未実装
        pass
