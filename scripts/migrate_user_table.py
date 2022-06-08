import boto3  # type: ignore
from boto3.dynamodb.conditions import Key  # type: ignore


def main() -> None:
    """
    ユーザのレビュー投稿数をbeeテーブルに追加する
    """
    stage = "dev"

    dynamodb = boto3.resource("dynamodb")

    bee_table = dynamodb.Table(f"bee-{stage}")

    users = bee_table.query(
        IndexName="GSI_0",
        KeyConditionExpression=Key("GSI_PK").eq("user"),
    )["Items"]

    new_table_items = []

    for user in users:

        reviews = bee_table.query(
            IndexName="GSI_1",
            KeyConditionExpression=Key("GSI_PK").eq("review")
            & Key("GSI_1_SK").eq(user["user_id"]),
        )["Items"]

        count = len(reviews)

        new_table_items.append(
            {
                **user,
                "GSI_3_SK": count,
                "post_review_count": count,
            }
        )

    with bee_table.batch_writer() as batch:
        for item in new_table_items:
            batch.put_item(Item=item)


if __name__ == "__main__":
    main()
