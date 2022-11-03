import os
from datetime import datetime, timedelta, timezone
from typing import Any, TypedDict

import boto3

from book_recommendation import train_and_predict


def lambda_handler(event, context):

    reviews = load_items_from_dynamodb("review")
    suggested_books = load_items_from_dynamodb("suggested_book")

    recommend_book = train_and_predict(reviews, suggested_books)

    japan_tz = timezone(timedelta(hours=9))
    created_at = datetime.now(japan_tz).isoformat(timespec="seconds")

    put_recommended_book_to_table(
        [
            {"user_id": k, "book_recommendations": v, "created_at": created_at}
            for k, v in recommend_book.items()
        ]
    )


def get_dynamodb_table():
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["DYNAMODB_TABLE"]
    return dynamodb.Table(table_name)


def load_items_from_dynamodb(item_id: str) -> list[Any]:

    table = get_dynamodb_table()

    def query(exclusive_start_key=None):
        option = {}
        if exclusive_start_key:
            option["ExclusiveStartKey"] = exclusive_start_key

        response = table.query(
            IndexName="GSI_0",
            KeyConditionExpression=boto3.dynamodb.conditions.Key("GSI_PK").eq(item_id),
            **option,
        )

        return response["Items"], response.get("LastEvaluatedKey")

    items, last_key = query()

    # レスポンスに LastEvaluatedKey が含まれなくなるまでループ処理を実行する
    # see https://dev.classmethod.jp/articles/hot-to-get-more-than-1mb-of-data-from-dynamodb-when-using-scan/
    while last_key is not None:
        new_items, last_key = query(exclusive_start_key=last_key)
        items.extend(new_items)

    return items


BookRecommendation = TypedDict(
    "BookRecommendation", {"ml_model_name": str, "isbn": str}
)

PutRecommendBookItem = TypedDict(
    "PutRecommendBookItem",
    {
        "user_id": str,
        "book_recommendations": list[BookRecommendation],
        "created_at": str,
    },
)


def put_recommended_book_to_table(items: list[PutRecommendBookItem]):

    table = get_dynamodb_table()

    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(
                Item={
                    "PK": f"book_recommendation#{item['user_id']}#{item['created_at']}",
                    "GSI_PK": "book_recommendation",
                    "GSI_0_SK": item["user_id"],
                    "GSI_1_SK": item["created_at"],
                    "GSI_2_SK": f"{item['user_id']}#{item['created_at']}",
                    "created_at": item["created_at"],
                    "user_id": item["user_id"],
                    "book_recommendations": item["book_recommendations"],
                }
            )
