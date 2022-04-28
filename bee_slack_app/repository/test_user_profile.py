# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name

import os

import boto3  # type: ignore
from moto import mock_dynamodb  # type: ignore

from bee_slack_app.repository.user_profile import UserProfile


@mock_dynamodb
class TestUserProfile:
    def setup_method(self, _):
        dynamodb = boto3.resource("dynamodb")

        self.table = dynamodb.create_table(
            TableName=os.environ["DYNAMODB_TABLE"],
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

    def test_レビューを作成できること(self):
        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id"
            ),
        )

        assert len(response["Items"]) == 0

        user_profile = UserProfile()

        user_profile.create(
            {
                "user_id": "test_user_id",
                "user_name": "永和　太郎",
                "department": "ＩＴＳ",
                "job_type": "技術職",
                "age_range": "20",
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

        assert actual["user_id"] == "user_id_0"
        assert actual["user_name"] == "永和　太郎"
        assert actual["department"] == "ＩＴＳ事業部"
        assert actual["job_type"] == "技術職"
        assert actual["age_range"] == "20"
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_ユーザー情報を上書きできること(self):
        user_profile = UserProfile()

        user_profile.create(
            {
                "user_id": "test_user_id",
                "user_name": "永和 花子",
                "department": "金融システム事業部",
                "job_type": "営業職",
                "age_range": "30",
                "updated_at": "2022-04-15T09:20:12+09:00",
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
        assert actual["user_name"] == "永和 花子"
        assert actual["department"] == "金融システム事業部"
        assert actual["job_type"] == "営業職"
        assert actual["age_range"] == "30"
        assert actual["updated_at"] == "2022-04-15T09:20:12+09:00"

        user_profile.create(
            {
                "user_id": "test_user_id",
                "user_name": "上書き次郎",
                "department": "金融システム事業部",
                "job_type": "管理職",
                "age_range": "50",
                "updated_at": "2022-04-28T09:32:14+09:00",
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
        assert actual["user_name"] == "上書き次郎"
        assert actual["department"] == "金融システム事業部"
        assert actual["job_type"] == "管理職"
        assert actual["age_range"] == "50"
        assert actual["updated_at"] == "2022-04-28T09:32:14+09:00"
