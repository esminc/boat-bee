# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name

import os

import boto3  # type: ignore
from moto import mock_dynamodb  # type: ignore

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

        user = user_repository.get("test_user_id_1")

        assert len(user) == 6

        assert user["user_id"] == "test_user_id_1"
        assert user["user_name"] == "問屋町　花子"
        assert user["department"] == "ＩＴＳ事業部"
        assert user["job_type"] == "管理職"
        assert user["age_range"] == "50"
        assert user["updated_at"] == "2022-04-11T09:23:04+09:00"

    def test_ユーザーが無い場合にNoneが返ること(self):  # pylint: disable=invalid-name
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

        user = user_repository.get("test_user_id_3")

        assert user is None

    def test_ユーザー情報が0件の場合にNoneを返すこと(self):  # pylint: disable=invalid-name
        # DBが空であることを確認
        response = self.table.scan()
        assert len(response["Items"]) == 0

        user_repository = UserRepository()
        user = user_repository.get("test_user_id_0")

        assert user is None

    def test_初期状態から最初のユーザー情報を作成できること(self):
        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id"
            ),
        )

        assert len(response["Items"]) == 0

        user_repository = UserRepository()

        user_repository.create(
            {
                "user_id": "test_user_id",
                "user_name": "永和　太郎",
                "department": "ＩＴＳ事業部",
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

        assert actual["user_id"] == "test_user_id"
        assert actual["user_name"] == "永和　太郎"
        assert actual["department"] == "ＩＴＳ事業部"
        assert actual["job_type"] == "技術職"
        assert actual["age_range"] == "20"
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_ユーザー情報を上書きできること(self):
        user_repository = UserRepository()

        user_repository.create(
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

        user_repository.create(
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

    def test_２件目以降のユーザー情報を作成できること(self):
        user_repository = UserRepository()

        user_repository.create(
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

        user_repository.create(
            {
                "user_id": "test_user_id_1",
                "user_name": "追加　小次郎",
                "department": "金融システム事業部",
                "job_type": "技術職",
                "age_range": "40",
                "updated_at": "2022-04-28T09:32:14+09:00",
            }
        )

        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id_1"
            ),
        )

        assert len(response["Items"]) == 1

        actual = response["Items"][0]

        assert actual["user_id"] == "test_user_id_1"
        assert actual["user_name"] == "追加　小次郎"
        assert actual["department"] == "金融システム事業部"
        assert actual["job_type"] == "技術職"
        assert actual["age_range"] == "40"
        assert actual["updated_at"] == "2022-04-28T09:32:14+09:00"

    def test_キー以外が同じ情報を追加で作成できること(self):
        user_repository = UserRepository()

        user_repository.create(
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

        user_repository.create(
            {
                "user_id": "test_user_id_1",
                "user_name": "永和 花子",
                "department": "金融システム事業部",
                "job_type": "営業職",
                "age_range": "30",
                "updated_at": "2022-04-15T09:20:12+09:00",
            }
        )

        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id_1"
            ),
        )

        assert len(response["Items"]) == 1

        actual = response["Items"][0]

        assert actual["user_id"] == "test_user_id_1"
        assert actual["user_name"] == "永和 花子"
        assert actual["department"] == "金融システム事業部"
        assert actual["job_type"] == "営業職"
        assert actual["age_range"] == "30"
        assert actual["updated_at"] == "2022-04-15T09:20:12+09:00"
