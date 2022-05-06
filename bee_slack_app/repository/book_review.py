import os
from typing import Optional, TypedDict

from boto3.dynamodb.conditions import Attr  # type: ignore

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.repository.database import get_database_client


# This is a sample
class BookReview:
    class GetConditions(TypedDict):
        score_for_me: Optional[str]
        score_for_others: Optional[str]

    def __init__(self):
        self.table = get_database_client().Table(os.environ["DYNAMODB_TABLE"])

    def get(self, conditions: GetConditions = None) -> list[ReviewContents]:
        """
        本のレビューを取得する

        Args:
            conditions : 検索条件。省略した場合は、全てのレビューを取得する。
        Returns:
            list[ReviewContents]: 本のレビューのリスト
        """

        def scan(exclusive_start_key=None, filter_expression=None):
            option = {}
            if filter_expression:
                option["FilterExpression"] = filter_expression
            if exclusive_start_key:
                option["ExclusiveStartKey"] = exclusive_start_key

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

        items, last_evaluated_key = scan(filter_expression=filter_expression)

        # レスポンスに LastEvaluatedKey が含まれなくなるまでループ処理を実行する
        # see https://dev.classmethod.jp/articles/hot-to-get-more-than-1mb-of-data-from-dynamodb-when-using-scan/
        while last_evaluated_key is not None:
            new_items, last_evaluated_key = scan(
                exclusive_start_key=last_evaluated_key,
                filter_expression=filter_expression,
            )
            items.extend(new_items)

        return items

    def create(self, review):
        item = {
            "user_id": review["user_id"],
            "book_title": review["book_title"],
            "isbn": review["isbn"],
            "score_for_me": review["score_for_me"],
            "score_for_others": review["score_for_others"],
            "review_comment": review["review_comment"],
            "updated_at": review["updated_at"],
        }

        self.table.put_item(Item=item)

        return item

    def delete(self):
        # 未実装
        pass
