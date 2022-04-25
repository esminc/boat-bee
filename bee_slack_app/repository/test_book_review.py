# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name

import os

import boto3  # type: ignore
from moto import mock_dynamodb  # type: ignore

from bee_slack_app.repository.book_review import BookReview


@mock_dynamodb
class TestBookReview:
    def setup_method(self, _):
        dynamodb = boto3.resource("dynamodb")

        self.table = dynamodb.create_table(
            TableName=os.environ["DYNAMODB_TABLE"],
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"},
                {"AttributeName": "isbn", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"},
                {"AttributeName": "isbn", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

    def test_レビューを取得できること(self):
        item = {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "user_id_2",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "2",
            "score_for_others": "4",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
        }

        self.table.put_item(Item=item)

        book_review = BookReview()

        reviews = book_review.get_all()

        assert len(reviews) == 3

        assert reviews[0]["user_id"] == "user_id_0"
        assert reviews[0]["isbn"] == "12345"
        assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[0]["score_for_me"] == "1"
        assert reviews[0]["score_for_others"] == "5"
        assert reviews[0]["review_comment"] == "とても良いです"

        assert reviews[1]["user_id"] == "user_id_1"
        assert reviews[1]["isbn"] == "12345"
        assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[1]["score_for_me"] == "3"
        assert reviews[1]["score_for_others"] == "4"
        assert reviews[1]["review_comment"] == "まあまあです"

        assert reviews[2]["user_id"] == "user_id_2"
        assert reviews[2]["isbn"] == "67890"
        assert reviews[2]["book_title"] == "Python チュートリアル"
        assert reviews[2]["score_for_me"] == "2"
        assert reviews[2]["score_for_others"] == "4"
        assert reviews[2]["review_comment"] == "そこそこです"

    def test_レビューが0件の場合_空配列を返すこと(self):
        response = self.table.scan()

        assert len(response["Items"]) == 0

        book_review = BookReview()

        reviews = book_review.get_all()

        assert len(reviews) == 0
        assert isinstance(reviews, list)

    def test_レビューを作成できること(self):
        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id"
            ),
        )

        assert len(response["Items"]) == 0

        book_review = BookReview()

        book_review.create(
            {
                "user_id": "test_user_id",
                "isbn": "12345",
                "book_title": "本のタイトル",
                "score_for_me": "1",
                "score_for_others": "3",
                "review_comment": "レビューコメント",
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )

        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id"
            ),
        )

        assert len(response["Items"]) == 1

        actual = response["Items"][0]

        assert actual["user_id"] == "test_user_id"
        assert actual["isbn"] == "12345"
        assert actual["book_title"] == "本のタイトル"
        assert actual["score_for_me"] == "1"
        assert actual["score_for_others"] == "3"
        assert actual["review_comment"] == "レビューコメント"
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_レビューを上書きできること(self):
        book_review = BookReview()

        book_review.create(
            {
                "user_id": "test_user_id",
                "isbn": "12345",
                "book_title": "最初のレビューのタイトル",
                "score_for_me": "1",
                "score_for_others": "3",
                "review_comment": "最初のレビューのコメント",
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )

        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id"
            ),
        )

        assert len(response["Items"]) == 1

        actual = response["Items"][0]

        assert actual["user_id"] == "test_user_id"
        assert actual["isbn"] == "12345"
        assert actual["book_title"] == "最初のレビューのタイトル"
        assert actual["score_for_me"] == "1"
        assert actual["score_for_others"] == "3"
        assert actual["review_comment"] == "最初のレビューのコメント"
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

        book_review.create(
            {
                "user_id": "test_user_id",
                "isbn": "12345",
                "book_title": "上書き後のレビューのタイトル",
                "score_for_me": "1",
                "score_for_others": "3",
                "review_comment": "上書き後のレビューのコメント",
                "updated_at": "2022-04-02T00:00:00+09:00",
            }
        )

        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id"
            ),
        )

        assert len(response["Items"]) == 1

        actual = response["Items"][0]

        assert actual["user_id"] == "test_user_id"
        assert actual["isbn"] == "12345"
        assert actual["book_title"] == "上書き後のレビューのタイトル"
        assert actual["score_for_me"] == "1"
        assert actual["score_for_others"] == "3"
        assert actual["review_comment"] == "上書き後のレビューのコメント"
        assert actual["updated_at"] == "2022-04-02T00:00:00+09:00"

    def test_同じuser_idで別々のisbnの場合_別々のアイテムとして登録すること(self):
        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id"
            ),
        )

        assert len(response["Items"]) == 0

        book_review = BookReview()

        book_review.create(
            {
                "user_id": "test_user_id",
                "isbn": "12345",
                "book_title": "本のタイトル",
                "score_for_me": "1",
                "score_for_others": "3",
                "review_comment": "レビューコメント",
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )

        book_review.create(
            {
                "user_id": "test_user_id",
                "isbn": "67890",
                "book_title": "本のタイトル",
                "score_for_me": "1",
                "score_for_others": "3",
                "review_comment": "レビューコメント",
                "updated_at": "2022-05-01T00:00:00+09:00",
            }
        )

        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id"
            ),
        )

        assert len(response["Items"]) == 2

        actual_0 = response["Items"][0]

        assert actual_0["user_id"] == "test_user_id"
        assert actual_0["isbn"] == "12345"
        assert actual_0["book_title"] == "本のタイトル"
        assert actual_0["score_for_me"] == "1"
        assert actual_0["score_for_others"] == "3"
        assert actual_0["review_comment"] == "レビューコメント"
        assert actual_0["updated_at"] == "2022-04-01T00:00:00+09:00"

        actual_1 = response["Items"][1]

        assert actual_1["user_id"] == "test_user_id"
        assert actual_1["isbn"] == "67890"
        assert actual_1["book_title"] == "本のタイトル"
        assert actual_1["score_for_me"] == "1"
        assert actual_1["score_for_others"] == "3"
        assert actual_1["review_comment"] == "レビューコメント"
        assert actual_1["updated_at"] == "2022-05-01T00:00:00+09:00"
