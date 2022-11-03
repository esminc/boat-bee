from typing import Optional, TypedDict

import boto3  # type: ignore

from bee_slack_app.repository import database

GSI_PK_VALUE = "book_recommendation"


BookRecommendation = TypedDict(
    "BookRecommendation", {"ml_model_name": str, "isbn": str}
)

RecommendBookRepositoryFetchResult = TypedDict(
    "RecommendBookRepositoryFetchResult",
    {
        "book_recommendations": list[BookRecommendation],
        "created_at": str,
    },
)


class RecommendBookRepository:  # pylint: disable=too-few-public-methods
    recommend_info = None

    def __init__(self) -> None:
        self.table = database.get_table()

    def fetch(self, user_id: str) -> Optional[RecommendBookRepositoryFetchResult]:
        items = self.table.query(
            IndexName=database.GSI_2,
            KeyConditionExpression=boto3.dynamodb.conditions.Key(database.GSI_PK).eq(
                GSI_PK_VALUE
            )
            & boto3.dynamodb.conditions.Key(database.GSI_2_SK).begins_with(user_id),
            ScanIndexForward=False,
            Limit=1,
        )["Items"]

        if len(items) == 0:
            return None

        item = items[0]  # 最新のおすすめデータを参照する

        book_recommendations: list[BookRecommendation] = [
            {
                "ml_model_name": book_recommendation["ml_model_name"],
                "isbn": book_recommendation["isbn"],
            }
            for book_recommendation in item["book_recommendations"]
        ]

        created_at = item["created_at"]

        return {
            "book_recommendations": book_recommendations,
            "created_at": created_at,
        }
