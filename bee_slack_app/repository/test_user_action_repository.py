# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name

import os

import boto3  # type: ignore
from moto import mock_dynamodb  # type: ignore

from bee_slack_app.model.user_action import UserAction
from bee_slack_app.repository.user_action_repository import UserActionRepository


@mock_dynamodb
class TestUserActionRepository:
    def setup_method(self, _):
        dynamodb = boto3.resource("dynamodb")

        self.table = dynamodb.create_table(
            TableName=os.environ["DYNAMODB_TABLE"] + "-user-action",
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"},
                {"AttributeName": "created_at", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"},
                {"AttributeName": "created_at", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

    def test_ユーザの行動履歴を保存できること(self):

        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "dummy_user_id_0"
            ),
        )

        assert len(response["Items"]) == 0

        user_action_repository = UserActionRepository()

        item: UserAction = {
            "user_id": "dummy_user_id_0",
            "created_at": "2022-04-01T00:00:00+09:00",
            "action_type": "dummy_action_type_0",
            "status": "dummy_status_0",
            "payload": None,
        }

        user_action_repository.put(item)

        item: UserAction = {
            "user_id": "dummy_user_id_1",
            "created_at": "2022-04-02T00:00:00+09:00",
            "action_type": "dummy_action_type_1",
            "status": "dummy_status_1",
            "payload": {"dummy_key": "dummy_value"},
        }

        user_action_repository.put(item)

        actual = self.table.get_item(
            Key={
                "user_id": "dummy_user_id_0",
                "created_at": "2022-04-01T00:00:00+09:00",
            }
        )["Item"]

        assert actual["user_id"] == "dummy_user_id_0"
        assert actual["created_at"] == "2022-04-01T00:00:00+09:00"
        assert actual["action_type"] == "dummy_action_type_0"
        assert actual["status"] == "dummy_status_0"
        assert actual["payload"] is None

        actual = self.table.get_item(
            Key={
                "user_id": "dummy_user_id_1",
                "created_at": "2022-04-02T00:00:00+09:00",
            }
        )["Item"]

        assert actual["user_id"] == "dummy_user_id_1"
        assert actual["created_at"] == "2022-04-02T00:00:00+09:00"
        assert actual["action_type"] == "dummy_action_type_1"
        assert actual["status"] == "dummy_status_1"
        assert actual["payload"] == {"dummy_key": "dummy_value"}
