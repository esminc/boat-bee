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
                {"AttributeName": "user_attribute_key", "AttributeType": "S"},
                {"AttributeName": "user_attribute_value", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "user_id", "KeyType": "HASH"},
                {"AttributeName": "user_attribute_key", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "UserTableGSI0",
                    "KeySchema": [
                        {"AttributeName": "user_attribute_value", "KeyType": "HASH"},
                        {"AttributeName": "user_id", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                }
            ],
        )

    def test_ユーザー情報を取得できること(self):
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "user_name",
            "user_attribute_value": "永和　太郎",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "department",
            "user_attribute_value": "ＩＴＳ事業部",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "job_type",
            "user_attribute_value": "技術職",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "age_range",
            "user_attribute_value": "20",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "updated_at",
            "user_attribute_value": "2022-04-01T00:00:00+09:00",
        }

        self.table.put_item(Item=item)

        user_repository = UserRepository()

        user = user_repository.get("test_user_id_0")

        assert user["user_id"] == "test_user_id_0"
        assert user["user_name"] == "永和　太郎"
        assert user["department"] == "ＩＴＳ事業部"
        assert user["job_type"] == "技術職"
        assert user["age_range"] == "20"
        assert user["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_複数のユーザー情報を取得できること(self):

        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "user_name",
            "user_attribute_value": "永和　太郎",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "department",
            "user_attribute_value": "ＩＴＳ事業部",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "job_type",
            "user_attribute_value": "技術職",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "age_range",
            "user_attribute_value": "20",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "updated_at",
            "user_attribute_value": "2022-04-01T00:00:00+09:00",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "post_review",
            "user_attribute_value": "post_review_true",
        }

        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_1",
            "user_attribute_key": "user_name",
            "user_attribute_value": "問屋町　花子",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_1",
            "user_attribute_key": "department",
            "user_attribute_value": "ＩＴＳ事業部",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_1",
            "user_attribute_key": "job_type",
            "user_attribute_value": "管理職",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_1",
            "user_attribute_key": "age_range",
            "user_attribute_value": "50",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_1",
            "user_attribute_key": "updated_at",
            "user_attribute_value": "2022-04-11T09:23:04+09:00",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_1",
            "user_attribute_key": "post_review",
            "user_attribute_value": "post_review_false",
        }

        self.table.put_item(Item=item)

        user_repository = UserRepository()

        users = user_repository.get_all()

        assert len(users) == 2

        assert users[0]["user_id"] == "test_user_id_0"
        assert users[0]["user_name"] == "永和　太郎"
        assert users[0]["department"] == "ＩＴＳ事業部"
        assert users[0]["job_type"] == "技術職"
        assert users[0]["age_range"] == "20"
        assert users[0]["updated_at"] == "2022-04-01T00:00:00+09:00"

        assert users[1]["user_id"] == "test_user_id_1"
        assert users[1]["user_name"] == "問屋町　花子"
        assert users[1]["department"] == "ＩＴＳ事業部"
        assert users[1]["job_type"] == "管理職"
        assert users[1]["age_range"] == "50"
        assert users[1]["updated_at"] == "2022-04-11T09:23:04+09:00"

    def test_レビューを投稿したユーザを取得できること(self):
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "user_name",
            "user_attribute_value": "永和　太郎",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "department",
            "user_attribute_value": "ＩＴＳ事業部",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "job_type",
            "user_attribute_value": "技術職",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "age_range",
            "user_attribute_value": "20",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "updated_at",
            "user_attribute_value": "2022-04-01T00:00:00+09:00",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "post_review",
            "user_attribute_value": "post_review_true",
        }

        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_1",
            "user_attribute_key": "user_name",
            "user_attribute_value": "問屋町　花子",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_1",
            "user_attribute_key": "department",
            "user_attribute_value": "ＩＴＳ事業部",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_1",
            "user_attribute_key": "job_type",
            "user_attribute_value": "管理職",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_1",
            "user_attribute_key": "age_range",
            "user_attribute_value": "50",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_1",
            "user_attribute_key": "updated_at",
            "user_attribute_value": "2022-04-11T09:23:04+09:00",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_1",
            "user_attribute_key": "post_review",
            "user_attribute_value": "post_review_false",
        }

        self.table.put_item(Item=item)

        user_repository = UserRepository()

        users = user_repository.get_by_posted_review()

        assert users[0]["user_id"] == "test_user_id_0"
        assert users[0]["user_name"] == "永和　太郎"
        assert users[0]["department"] == "ＩＴＳ事業部"
        assert users[0]["job_type"] == "技術職"
        assert users[0]["age_range"] == "20"
        assert users[0]["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_ユーザを作成できること(self):
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

        items = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id"
            ),
        )["Items"]

        user = {
            item["user_attribute_key"]: item["user_attribute_value"] for item in items
        }

        assert user == {
            "user_name": "永和　太郎",
            "department": "ＩＴＳ事業部",
            "job_type": "技術職",
            "age_range": "20",
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

    def test_レビューを投稿しているかを更新できること(self):
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "user_name",
            "user_attribute_value": "永和　太郎",
        }

        self.table.put_item(Item=item)

        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "department",
            "user_attribute_value": "ＩＴＳ事業部",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "job_type",
            "user_attribute_value": "技術職",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "age_range",
            "user_attribute_value": "20",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "updated_at",
            "user_attribute_value": "2022-04-01T00:00:00+09:00",
        }
        self.table.put_item(Item=item)
        item = {
            "user_id": "test_user_id_0",
            "user_attribute_key": "post_review",
            "user_attribute_value": "post_review_false",
        }
        self.table.put_item(Item=item)

        items = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id_0"
            ),
        )["Items"]

        user = {
            item["user_attribute_key"]: item["user_attribute_value"] for item in items
        }

        assert user == {
            "user_name": "永和　太郎",
            "department": "ＩＴＳ事業部",
            "job_type": "技術職",
            "age_range": "20",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "post_review": "post_review_false",
        }

        user_repository = UserRepository()

        user_repository.update_posted_review(
            user_id="test_user_id_0", posted_review=True
        )

        items = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id_0"
            ),
        )["Items"]

        user = {
            item["user_attribute_key"]: item["user_attribute_value"] for item in items
        }

        assert user == {
            "user_name": "永和　太郎",
            "department": "ＩＴＳ事業部",
            "job_type": "技術職",
            "age_range": "20",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "post_review": "post_review_true",
        }
