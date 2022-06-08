import boto3  # type: ignore


def main() -> None:
    """
    テーブルを一つにまとめる
    """

    dynamodb = boto3.resource("dynamodb")

    stage = "dev"

    new_table_items = []

    book_table = dynamodb.Table(f"bee-{stage}-book")

    for item in book_table.scan()["Items"]:
        new_table_items.append(
            {
                "PK": "book#" + item["isbn"],
                "GSI_PK": "book",
                "GSI_0_SK": item["updated_at"],
                "isbn": item["isbn"],
                "title": item["title"],
                "author": item["author"],
                "url": item["url"],
                "image_url": item["image_url"],
                "description": item["description"],
                "updated_at": item["updated_at"],
            }
        )

    user_table = dynamodb.Table(f"bee-{stage}-user")

    for item in user_table.scan()["Items"]:
        new_table_items.append(
            {
                "PK": "user#" + item["user_id"],
                "GSI_PK": "user",
                "GSI_0_SK": item["updated_at"],
                "user_id": item["user_id"],
                "user_name": item["user_name"],
                "department": item["department"],
                "job_type": item["job_type"],
                "age_range": item["age_range"],
                "updated_at": item["updated_at"],
            }
        )

    review_table = dynamodb.Table(f"bee-{stage}-review")

    for item in review_table.scan()["Items"]:
        new_table_items.append(
            {
                "PK": "review#" + item["user_id"] + "#" + item["isbn"],
                "GSI_PK": "review",
                "GSI_0_SK": item["updated_at"],
                "GSI_1_SK": item["user_id"],
                "GSI_2_SK": item["isbn"],
                "user_id": item["user_id"],
                "book_title": item["book_title"],
                "isbn": item["isbn"],
                "score_for_me": item["score_for_me"],
                "score_for_others": item["score_for_others"],
                "review_comment": item["review_comment"],
                "updated_at": item["updated_at"],
                "book_image_url": item["book_image_url"],
                "book_author": item["book_author"],
                "book_url": item["book_url"],
                "book_description": item["book_description"],
            }
        )

    user_action_table = dynamodb.Table(f"bee-{stage}-user-action")

    for item in user_action_table.scan()["Items"]:
        new_table_items.append(
            {
                "PK": "user_action#" + item["user_id"] + "#" + item["created_at"],
                "GSI_PK": "user_action",
                "GSI_0_SK": item["created_at"],
                "GSI_1_SK": item["user_id"],
                "user_id": item["user_id"],
                "created_at": item["created_at"],
                "action_name": item["action_name"],
                "status": item["status"],
                "payload": item["payload"],
            }
        )

    suggested_book_table = dynamodb.Table(f"bee-{stage}-suggested-book")

    for item in suggested_book_table.scan()["Items"]:
        new_table_items.append(
            {
                "PK": "suggested_book#"
                + item["user_id"]
                + "#"
                + item["isbn"]
                + "#"
                + item["ml_model"],
                "GSI_PK": "suggested_book",
                "GSI_0_SK": item["updated_at"],
                "GSI_1_SK": item["isbn"],
                "GSI_2_SK": item["ml_model"],
                "user_id": item["user_id"],
                "isbn": item["isbn"],
                "ml_model": item["ml_model"],
                "interested": item["interested"],
                "updated_at": item["updated_at"],
            }
        )

    bee_table = dynamodb.Table(f"bee-{stage}")

    with bee_table.batch_writer() as batch:
        for item in new_table_items:
            batch.put_item(Item=item)


if __name__ == "__main__":
    main()
