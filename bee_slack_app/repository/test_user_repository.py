# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name

import os

import boto3  # type: ignore
from moto import mock_dynamodb

from bee_slack_app.repository.user_repository import UserRepository


@mock_dynamodb
class TestUserRepository:
    def setup_method(self, _):
        dynamodb = boto3.resource("dynamodb")

        self.table = dynamodb.create_table(
            TableName=os.environ["DYNAMODB_TABLE"] + "-user",
            AttributeDefinitions=[
                {"AttributeName": "user_id", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )

    def test_ユーザー情報を取得できること(self):
        item = {
            "user_id": "test_user_id_0",
            "user_name": "永和　太郎",
            "department": "ＩＴＳ事業部",
            "job_type": "技術職",
            "age_range": "20",
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_1",
            "user_name": "問屋町　花子",
            "department": "ＩＴＳ事業部",
            "job_type": "管理職",
            "age_range": "50",
            "updated_at": "2022-04-11T09:23:04+09:00",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_2",
            "user_name": "北ノ庄　肇",
            "department": "金融システム事業部",
            "job_type": "営業職",
            "age_range": "30",
            "updated_at": "2022-05-02T16:43:25+09:00",
        }

        self.table.put_item(Item=item)

        user_repository = UserRepository()

        users = user_repository.get_user("test_user_id_1")

        assert len(users) == 6

        assert users["user_id"] == "test_user_id_1"
        assert users["user_name"] == "問屋町　花子"
        assert users["department"] == "ＩＴＳ事業部"
        assert users["job_type"] == "管理職"
        assert users["age_range"] == "50"
        assert users["updated_at"] == "2022-04-11T09:23:04+09:00"


"""
    def test_ユーザー情報が0件の場合_空配列を返すこと(self):
        response = self.table.scan()

        assert len(response["Items"]) == 0

        user_repository = UserRepository()

        users = user_repository.get_user("test_user_id_0")

        assert len(users) == 0
        assert isinstance(users, list)
"""
