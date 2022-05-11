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
            TableName=os.environ["DYNAMODB_TABLE"] + "-review",
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
            "image_url": "dummy_image_url_0",
            "author": "dummy_author_0",
            "url": "dummy_url_0",
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
            "image_url": "dummy_image_url_1",
            "author": "dummy_author_1",
            "url": "dummy_url_1",
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
            "image_url": "dummy_image_url_2",
            "author": "dummy_author_2",
            "url": "dummy_url_2",
        }

        self.table.put_item(Item=item)

        book_review = BookReview()

        reviews = book_review.get()

        assert len(reviews) == 3

        assert reviews[0]["user_id"] == "user_id_0"
        assert reviews[0]["isbn"] == "12345"
        assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[0]["score_for_me"] == "1"
        assert reviews[0]["score_for_others"] == "5"
        assert reviews[0]["review_comment"] == "とても良いです"
        assert reviews[0]["image_url"] == "dummy_image_url_0"
        assert reviews[0]["author"] == "dummy_author_0"
        assert reviews[0]["url"] == "dummy_url_0"

        assert reviews[1]["user_id"] == "user_id_1"
        assert reviews[1]["isbn"] == "12345"
        assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[1]["score_for_me"] == "3"
        assert reviews[1]["score_for_others"] == "4"
        assert reviews[1]["review_comment"] == "まあまあです"
        assert reviews[1]["image_url"] == "dummy_image_url_1"
        assert reviews[1]["author"] == "dummy_author_1"
        assert reviews[1]["url"] == "dummy_url_1"

        assert reviews[2]["user_id"] == "user_id_2"
        assert reviews[2]["isbn"] == "67890"
        assert reviews[2]["book_title"] == "Python チュートリアル"
        assert reviews[2]["score_for_me"] == "2"
        assert reviews[2]["score_for_others"] == "4"
        assert reviews[2]["review_comment"] == "そこそこです"
        assert reviews[2]["image_url"] == "dummy_image_url_2"
        assert reviews[2]["author"] == "dummy_author_2"
        assert reviews[2]["url"] == "dummy_url_2"

    def test_レビューが0件の場合_空配列を返すこと(self):
        response = self.table.scan()

        assert len(response["Items"]) == 0

        book_review = BookReview()

        reviews = book_review.get()

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
                "image_url": "dummy_image_url",
                "author": "dummy_author",
                "url": "dummy_url",
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
        assert actual["image_url"] == "dummy_image_url"
        assert actual["author"] == "dummy_author"
        assert actual["url"] == "dummy_url"

    def test_自分にとっての評価を指定してレビューを取得できること(self):
        item = {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "image_url": "dummy_image_url_0",
            "author": "dummy_author_0",
            "url": "dummy_url_0",
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
            "image_url": "dummy_image_url_1",
            "author": "dummy_author_1",
            "url": "dummy_url_1",
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
            "image_url": "dummy_image_url_2",
            "author": "dummy_author_2",
            "url": "dummy_url_2",
        }

        self.table.put_item(Item=item)

        book_review = BookReview()

        reviews = book_review.get({"score_for_me": 3})

        assert len(reviews) == 2

        assert reviews[0]["user_id"] == "user_id_0"
        assert reviews[0]["isbn"] == "12345"
        assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[0]["score_for_me"] == "3"
        assert reviews[0]["score_for_others"] == "5"
        assert reviews[0]["review_comment"] == "とても良いです"
        assert reviews[0]["image_url"] == "dummy_image_url_0"
        assert reviews[0]["author"] == "dummy_author_0"
        assert reviews[0]["url"] == "dummy_url_0"

        assert reviews[1]["user_id"] == "user_id_1"
        assert reviews[1]["isbn"] == "12345"
        assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[1]["score_for_me"] == "3"
        assert reviews[1]["score_for_others"] == "4"
        assert reviews[1]["review_comment"] == "まあまあです"
        assert reviews[1]["image_url"] == "dummy_image_url_1"
        assert reviews[1]["author"] == "dummy_author_1"
        assert reviews[1]["url"] == "dummy_url_1"

    def test_他の人へのおすすめ度を指定してレビューを取得できること(self):
        item = {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "image_url": "dummy_image_url_0",
            "author": "dummy_author_0",
            "url": "dummy_url_0",
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
            "image_url": "dummy_image_url_1",
            "author": "dummy_author_1",
            "url": "dummy_url_1",
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
            "image_url": "dummy_image_url_2",
            "author": "dummy_author_2",
            "url": "dummy_url_2",
        }

        self.table.put_item(Item=item)

        book_review = BookReview()

        reviews = book_review.get({"score_for_others": 4})

        assert len(reviews) == 2

        assert reviews[0]["user_id"] == "user_id_1"
        assert reviews[0]["isbn"] == "12345"
        assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[0]["score_for_me"] == "3"
        assert reviews[0]["score_for_others"] == "4"
        assert reviews[0]["review_comment"] == "まあまあです"
        assert reviews[0]["image_url"] == "dummy_image_url_1"
        assert reviews[0]["author"] == "dummy_author_1"
        assert reviews[0]["url"] == "dummy_url_1"

        assert reviews[1]["user_id"] == "user_id_2"
        assert reviews[1]["isbn"] == "67890"
        assert reviews[1]["book_title"] == "Python チュートリアル"
        assert reviews[1]["score_for_me"] == "2"
        assert reviews[1]["score_for_others"] == "4"
        assert reviews[1]["review_comment"] == "そこそこです"
        assert reviews[1]["image_url"] == "dummy_image_url_2"
        assert reviews[1]["author"] == "dummy_author_2"
        assert reviews[1]["url"] == "dummy_url_2"

    def test_自分にとっての評価と他の人へのおすすめ度を指定してレビューを取得できること(self):
        item = {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "image_url": "dummy_image_url_0",
            "author": "dummy_author_0",
            "url": "dummy_url_0",
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
            "image_url": "dummy_image_url_1",
            "author": "dummy_author_1",
            "url": "dummy_url_1",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "user_id_2",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "3",
            "score_for_others": "5",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
            "image_url": "dummy_image_url_2",
            "author": "dummy_author_2",
            "url": "dummy_url_2",
        }

        self.table.put_item(Item=item)

        book_review = BookReview()

        reviews = book_review.get({"score_for_me": 3, "score_for_others": 5})

        assert len(reviews) == 2

        assert reviews[0]["user_id"] == "user_id_0"
        assert reviews[0]["isbn"] == "12345"
        assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[0]["score_for_me"] == "3"
        assert reviews[0]["score_for_others"] == "5"
        assert reviews[0]["review_comment"] == "とても良いです"
        assert reviews[0]["image_url"] == "dummy_image_url_0"
        assert reviews[0]["author"] == "dummy_author_0"
        assert reviews[0]["url"] == "dummy_url_0"

        assert reviews[1]["user_id"] == "user_id_2"
        assert reviews[1]["isbn"] == "67890"
        assert reviews[1]["book_title"] == "Python チュートリアル"
        assert reviews[1]["score_for_me"] == "3"
        assert reviews[1]["score_for_others"] == "5"
        assert reviews[1]["review_comment"] == "そこそこです"
        assert reviews[1]["image_url"] == "dummy_image_url_2"
        assert reviews[1]["author"] == "dummy_author_2"
        assert reviews[1]["url"] == "dummy_url_2"

    def test_検索条件を指定してレビューが0件の場合_空配列を返すこと(self):
        item = {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "image_url": "dummy_image_url_0",
            "author": "dummy_author_0",
            "url": "dummy_url_0",
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
            "image_url": "dummy_image_url_1",
            "author": "dummy_author_1",
            "url": "dummy_url_1",
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
            "image_url": "dummy_image_url_2",
            "author": "dummy_author_2",
            "url": "dummy_url_2",
        }

        book_review = BookReview()

        reviews = book_review.get({"score_for_others": 1})

        assert len(reviews) == 0
        assert isinstance(reviews, list)

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
                "image_url": "dummy_image_url",
                "author": "dummy_author",
                "url": "dummy_url",
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
        assert actual["image_url"] == "dummy_image_url"
        assert actual["author"] == "dummy_author"
        assert actual["url"] == "dummy_url"

        book_review.create(
            {
                "user_id": "test_user_id",
                "isbn": "12345",
                "book_title": "上書き後のレビューのタイトル",
                "score_for_me": "1",
                "score_for_others": "3",
                "review_comment": "上書き後のレビューのコメント",
                "updated_at": "2022-04-02T00:00:00+09:00",
                "image_url": "dummy_image_url",
                "author": "dummy_author",
                "url": "dummy_url",
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
        assert actual["image_url"] == "dummy_image_url"
        assert actual["author"] == "dummy_author"
        assert actual["url"] == "dummy_url"

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
                "image_url": "dummy_image_url_0",
                "author": "dummy_author_0",
                "url": "dummy_url_0",
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
                "image_url": "dummy_image_url_1",
                "author": "dummy_author_1",
                "url": "dummy_url_1",
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
        assert actual_0["image_url"] == "dummy_image_url_0"
        assert actual_0["author"] == "dummy_author_0"
        assert actual_0["url"] == "dummy_url_0"

        actual_1 = response["Items"][1]

        assert actual_1["user_id"] == "test_user_id"
        assert actual_1["isbn"] == "67890"
        assert actual_1["book_title"] == "本のタイトル"
        assert actual_1["score_for_me"] == "1"
        assert actual_1["score_for_others"] == "3"
        assert actual_1["review_comment"] == "レビューコメント"
        assert actual_1["updated_at"] == "2022-05-01T00:00:00+09:00"
        assert actual_1["image_url"] == "dummy_image_url_1"
        assert actual_1["author"] == "dummy_author_1"
        assert actual_1["url"] == "dummy_url_1"
