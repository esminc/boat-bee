from datetime import datetime

import boto3  # type: ignore


def main() -> None:
    """
    レビューが投稿されている本をbookテーブルに追加する
    """

    dynamodb = boto3.resource("dynamodb")

    stage = "dev"

    review_table = dynamodb.Table(f"bee-{stage}-review")
    book_table = dynamodb.Table(f"bee-{stage}-book")

    books = []
    reviews = review_table.scan()["Items"]

    for review in reviews:

        updated_at = str(
            datetime.max.timestamp()
            - datetime.fromisoformat(review["updated_at"]).timestamp()
        )

        book = {
            "book_pk": "book_pk_value",
            "isbn": review["isbn"],
            "title": review["book_title"],
            "author": review["book_author"],
            "url": review["book_url"],
            "image_url": review["book_image_url"],
            "description": review["book_description"],
            "updated_at": updated_at,
        }

        books.append(book)

    with book_table.batch_writer() as batch:
        for book in books:
            batch.put_item(Item=book)


if __name__ == "__main__":
    main()
