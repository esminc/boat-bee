# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name

import os

import boto3  # type: ignore
from moto import mock_dynamodb  # type: ignore

from bee_slack_app.repository.suggested_book_repository import SuggestedBookRepository


@mock_dynamodb
class TestSuggestedBookRepository:
    def setup_method(self, _):
        dynamodb = boto3.resource("dynamodb")

        self.table = dynamodb.create_table(
            TableName=os.environ["DYNAMODB_TABLE"] + "-suggested-book",
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"},
                {"AttributeName": "suggested_book_sk", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"},
                {"AttributeName": "suggested_book_sk", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

    def test_ＤＢの先頭にあるおすすめされた本を取得できること(self):
        item = {
            "user_id": "test_user_id_0",
            "suggested_book_sk": "1234567890123#dummy_ml_model_0",
            "interested": True,
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_1",
            "suggested_book_sk": "9234567890123#dummy_ml_model_1",
            "interested": True,
            "updated_at": "2022-04-11T09:23:04+09:00",
        }

        self.table.put_item(Item=item)

        suggested_book_repository = SuggestedBookRepository()

        suggested_book = suggested_book_repository.get(
            "test_user_id_0", "1234567890123", "dummy_ml_model_0"
        )

        assert suggested_book["user_id"] == "test_user_id_0"
        assert suggested_book["isbn"] == "1234567890123"
        assert suggested_book["ml_model"] == "dummy_ml_model_0"
        assert suggested_book["interested"] is True
        assert suggested_book["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_ＤＢの最後尾にあるおすすめされた本を取得できること(self):
        item = {
            "user_id": "test_user_id_0",
            "suggested_book_sk": "1234567890123#dummy_ml_model_0",
            "interested": True,
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_1",
            "suggested_book_sk": "9234567890123#dummy_ml_model_1",
            "interested": False,
            "updated_at": "2022-04-11T09:23:04+09:00",
        }

        self.table.put_item(Item=item)

        suggested_book_repository = SuggestedBookRepository()

        suggested_book = suggested_book_repository.get(
            "test_user_id_1", "9234567890123", "dummy_ml_model_1"
        )

        assert suggested_book["user_id"] == "test_user_id_1"
        assert suggested_book["isbn"] == "9234567890123"
        assert suggested_book["ml_model"] == "dummy_ml_model_1"
        assert suggested_book["interested"] is False
        assert suggested_book["updated_at"] == "2022-04-11T09:23:04+09:00"

    def test_おすすめされた本が無い場合にNoneが返ること(self):
        item = {
            "user_id": "test_user_id_0",
            "suggested_book_sk": "1234567890123#dummy_ml_model_0",
            "interested": True,
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_1",
            "suggested_book_sk": "9234567890123#dummy_ml_model_1",
            "interested": False,
            "updated_at": "2022-04-11T09:23:04+09:00",
        }

        self.table.put_item(Item=item)

        suggested_book_repository = SuggestedBookRepository()

        suggested_book = suggested_book_repository.get(
            "test_user_id_0", "9234567890123", "dummy_ml_model_1"
        )

        assert suggested_book is None
