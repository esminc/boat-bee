# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name

import os

import boto3  # type: ignore
from moto import mock_dynamodb  # type: ignore

from bee_slack_app.model.book import Book
from bee_slack_app.repository.book_repository import BookRepository


@mock_dynamodb
class TestBookRepository:
    def setup_method(self, _):
        dynamodb = boto3.resource("dynamodb")

        self.table = dynamodb.create_table(
            TableName=os.environ["DYNAMODB_TABLE"] + "-book",
            AttributeDefinitions=[
                {"AttributeName": "book_pk", "AttributeType": "S"},
                {"AttributeName": "isbn", "AttributeType": "S"},
                {"AttributeName": "updated_at", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "book_pk", "KeyType": "HASH"},
                {"AttributeName": "isbn", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "updatedAtIndex",
                    "KeySchema": [
                        {"AttributeName": "book_pk", "KeyType": "HASH"},
                        {"AttributeName": "updated_at", "KeyType": "RANGE"},
                    ],
                    "Projection": {
                        "ProjectionType": "ALL",
                    },
                }
            ],
        )

    def test_本を保存できること(self):

        book_repository = BookRepository()

        item: Book = {
            "isbn": "12345",
            "title": "dummy_title",
            "author": "dummy_author",
            "url": "dummy_url",
            "image_url": "dummy_image_url",
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

        book_repository.put(book=item)

        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("book_pk").eq(
                "book_pk_value"
            ),
        )

        books_items = response["Items"]

        assert books_items[0]["book_pk"] == "book_pk_value"
        assert books_items[0]["isbn"] == "12345"
        assert books_items[0]["updated_at"] == "251753562000.0"
        assert books_items[0]["title"] == "dummy_title"
        assert books_items[0]["author"] == "dummy_author"
        assert books_items[0]["url"] == "dummy_url"
        assert books_items[0]["image_url"] == "dummy_image_url"

    def test_本を取得できること(self):
        item = {
            "book_pk": "book_pk_value",
            "isbn": "12345",
            "updated_at": "251753562000.0",
            "title": "dummy_title_0",
            "author": "dummy_author_0",
            "url": "dummy_url_0",
            "image_url": "dummy_image_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "book_pk": "book_pk_value",
            "isbn": "67890",
            "updated_at": "251753475600.0",
            "title": "dummy_title_1",
            "author": "dummy_author_1",
            "url": "dummy_url_1",
            "image_url": "dummy_image_url_1",
        }

        self.table.put_item(Item=item)

        item = {
            "book_pk": "book_pk_value",
            "isbn": "01234",
            "updated_at": "251753389200.0",
            "title": "dummy_title_2",
            "author": "dummy_author_2",
            "url": "dummy_url_2",
            "image_url": "dummy_image_url_2",
        }

        self.table.put_item(Item=item)

        book_repository = BookRepository()

        books = book_repository.fetch()

        books_items = books["items"]

        assert len(books_items) == 3

        assert books_items[0]["isbn"] == "01234"
        assert books_items[0]["title"] == "dummy_title_2"
        assert books_items[0]["author"] == "dummy_author_2"
        assert books_items[0]["url"] == "dummy_url_2"
        assert books_items[0]["image_url"] == "dummy_image_url_2"
        assert books_items[0]["updated_at"] == "2022-04-03T00:00:00+09:00"

        assert books_items[1]["isbn"] == "67890"
        assert books_items[1]["title"] == "dummy_title_1"
        assert books_items[1]["author"] == "dummy_author_1"
        assert books_items[1]["url"] == "dummy_url_1"
        assert books_items[1]["image_url"] == "dummy_image_url_1"
        assert books_items[1]["updated_at"] == "2022-04-02T00:00:00+09:00"

        assert books_items[2]["isbn"] == "12345"
        assert books_items[2]["title"] == "dummy_title_0"
        assert books_items[2]["author"] == "dummy_author_0"
        assert books_items[2]["url"] == "dummy_url_0"
        assert books_items[2]["image_url"] == "dummy_image_url_0"
        assert books_items[2]["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_複数回に分けて本を取得できること(self):
        item = {
            "book_pk": "book_pk_value",
            "isbn": "12345",
            "updated_at": "251753562000.0",
            "title": "dummy_title_0",
            "author": "dummy_author_0",
            "url": "dummy_url_0",
            "image_url": "dummy_image_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "book_pk": "book_pk_value",
            "isbn": "67890",
            "updated_at": "251753475600.0",
            "title": "dummy_title_1",
            "author": "dummy_author_1",
            "url": "dummy_url_1",
            "image_url": "dummy_image_url_1",
        }

        self.table.put_item(Item=item)

        item = {
            "book_pk": "book_pk_value",
            "isbn": "01234",
            "updated_at": "251753389200.0",
            "title": "dummy_title_2",
            "author": "dummy_author_2",
            "url": "dummy_url_2",
            "image_url": "dummy_image_url_2",
        }

        self.table.put_item(Item=item)

        book_repository = BookRepository()

        # 1回目
        books = book_repository.fetch(limit=2)

        books_items = books["items"]

        assert len(books_items) == 2

        assert books_items[0]["isbn"] == "01234"
        assert books_items[0]["title"] == "dummy_title_2"
        assert books_items[0]["author"] == "dummy_author_2"
        assert books_items[0]["url"] == "dummy_url_2"
        assert books_items[0]["image_url"] == "dummy_image_url_2"
        assert books_items[0]["updated_at"] == "2022-04-03T00:00:00+09:00"

        assert books_items[1]["isbn"] == "67890"
        assert books_items[1]["title"] == "dummy_title_1"
        assert books_items[1]["author"] == "dummy_author_1"
        assert books_items[1]["url"] == "dummy_url_1"
        assert books_items[1]["image_url"] == "dummy_image_url_1"
        assert books_items[1]["updated_at"] == "2022-04-02T00:00:00+09:00"

        # 2回目
        books = book_repository.fetch(limit=2, start_key=books["last_key"])

        books_items = books["items"]

        assert len(books_items) == 1

        assert books_items[0]["isbn"] == "12345"
        assert books_items[0]["title"] == "dummy_title_0"
        assert books_items[0]["author"] == "dummy_author_0"
        assert books_items[0]["url"] == "dummy_url_0"
        assert books_items[0]["image_url"] == "dummy_image_url_0"
        assert books_items[0]["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_本が存在しない場合は空配列を返すこと(self):  # pylint: disable=invalid-name
        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("book_pk").eq(
                "book_pk_value"
            ),
        )

        assert len(response["Items"]) == 0

        book_repository = BookRepository()

        books = book_repository.fetch()

        books_items = books["items"]
        books_last_key = books["last_key"]

        assert len(books_items) == 0
        assert books_last_key is None
