import os
from typing import Optional, TypedDict

from boto3.dynamodb.conditions import Attr  # type: ignore

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.repository.database import get_database_client


class ReviewItemKey(TypedDict):
    user_id: str
    isbn: str


class GetResponse(TypedDict):
    items: list[ReviewContents]
    last_key: Optional[ReviewItemKey]


# This is a sample
class BookReview:
    class GetConditions(TypedDict):
        score_for_me: Optional[str]
        score_for_others: Optional[str]

    def __init__(self):
        self.table = get_database_client().Table(
            os.environ["DYNAMODB_TABLE"] + "-review"
        )

    def get(
        self,
        *,
        conditions: GetConditions = None,
        limit: Optional[int] = None,
        start_key: Optional[ReviewItemKey] = None,
    ) -> GetResponse:
        """
        本のレビューを取得する

        Args:
            conditions : 検索条件。省略した場合は、全てのレビューを取得する。
            limit : 取得するアイテムの上限数
            start_key: 読み込み位置を表すキー
        Returns:
            items: 本のレビューのリスト
            last_key: 読み込んだ最後のキー
        """

        def scan(exclusive_start_key=None, filter_expression=None, max_item_count=None):
            option = {}
            if filter_expression:
                option["FilterExpression"] = filter_expression
            if exclusive_start_key:
                option["ExclusiveStartKey"] = exclusive_start_key
            if max_item_count:
                option["Limit"] = max_item_count

            response = self.table.scan(**option)

            return response["Items"], response.get("LastEvaluatedKey")

        filter_expression = None

        if conditions:
            for condition_key, condition_value in conditions.items():
                filter_expression = (
                    filter_expression & Attr(condition_key).eq(str(condition_value))
                    if filter_expression
                    else Attr(condition_key).eq(str(condition_value))
                )

        items, last_key = scan(
            filter_expression=filter_expression,
            exclusive_start_key=start_key,
            max_item_count=limit,
        )

        if not limit:
            # レスポンスに LastEvaluatedKey が含まれなくなるまでループ処理を実行する
            # see https://dev.classmethod.jp/articles/hot-to-get-more-than-1mb-of-data-from-dynamodb-when-using-scan/
            while last_key is not None:
                new_items, last_key = scan(exclusive_start_key=last_key)
                items.extend(new_items)

        return {"items": items, "last_key": last_key}

    def create(self, review):
        item = {
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
        }

        self.table.put_item(Item=item)

        return item

    def delete(self):
        # 未実装
        pass
