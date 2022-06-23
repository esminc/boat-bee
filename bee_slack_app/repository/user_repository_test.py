# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name
# pylint: disable=invalid-name

from moto import mock_dynamodb  # type: ignore

from bee_slack_app.repository.database import create_table
from bee_slack_app.repository.user_repository import UserRepository


@mock_dynamodb
class TestUserRepository:
    def setup_method(self, _):
        self.table = create_table()

    def test_ユーザー情報を取得できること(self):
        item = {
            "PK": "user#test_user_id_0",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_3_SK": 1,
            "user_id": "test_user_id_0",
            "user_name": "永和　太郎",
            "department": "ＩＴＳ事業部",
            "job_type": "技術職",
            "age_range": "20",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "post_review_count": 1,
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "user#test_user_id_1",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-04-11T09:23:04+09:00",
            "GSI_3_SK": 0,
            "user_id": "test_user_id_1",
            "user_name": "問屋町　花子",
            "department": "ＩＴＳ事業部",
            "job_type": "管理職",
            "age_range": "50",
            "updated_at": "2022-04-11T09:23:04+09:00",
            "post_review_count": 0,
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "user#test_user_id_2",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-05-02T16:43:25+09:00",
            "GSI_3_SK": 0,
            "user_id": "test_user_id_2",
            "user_name": "北ノ庄　肇",
            "department": "金融システム事業部",
            "job_type": "営業職",
            "age_range": "30",
            "updated_at": "2022-05-02T16:43:25+09:00",
            "post_review_count": 0,
        }

        self.table.put_item(Item=item)

        user_repository = UserRepository()

        user = user_repository.get("test_user_id_1")

        assert user["user_id"] == "test_user_id_1"
        assert user["user_name"] == "問屋町　花子"
        assert user["department"] == "ＩＴＳ事業部"
        assert user["job_type"] == "管理職"
        assert user["age_range"] == "50"
        assert user["updated_at"] == "2022-04-11T09:23:04+09:00"

    def test_ユーザーが無い場合にNoneが返ること(self):
        item = {
            "PK": "user#test_user_id_0",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_3_SK": 1,
            "user_id": "test_user_id_0",
            "user_name": "永和　太郎",
            "department": "ＩＴＳ事業部",
            "job_type": "技術職",
            "age_range": "20",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "post_review_count": 1,
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "user#test_user_id_1",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-04-11T09:23:04+09:00",
            "GSI_3_SK": 0,
            "user_id": "test_user_id_1",
            "user_name": "問屋町　花子",
            "department": "ＩＴＳ事業部",
            "job_type": "管理職",
            "age_range": "50",
            "updated_at": "2022-04-11T09:23:04+09:00",
            "post_review_count": 0,
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "user#test_user_id_2",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-05-02T16:43:25+09:00",
            "GSI_3_SK": 0,
            "user_id": "test_user_id_2",
            "user_name": "北ノ庄　肇",
            "department": "金融システム事業部",
            "job_type": "営業職",
            "age_range": "30",
            "updated_at": "2022-05-02T16:43:25+09:00",
            "post_review_count": 0,
        }

        self.table.put_item(Item=item)

        user_repository = UserRepository()

        user = user_repository.get("test_user_id_3")

        assert user is None

    def test_ユーザー情報が0件の場合にNoneを返すこと(self):
        # DBが空であることを確認
        response = self.table.scan()
        assert len(response["Items"]) == 0

        user_repository = UserRepository()
        user = user_repository.get("test_user_id_0")

        assert user is None

    def test_複数のユーザー情報を取得できること(self):
        item = {
            "PK": "user#test_user_id_0",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_3_SK": 1,
            "user_id": "test_user_id_0",
            "user_name": "永和　太郎",
            "department": "ＩＴＳ事業部",
            "job_type": "技術職",
            "age_range": "20",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "post_review_count": 1,
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "user#test_user_id_1",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-04-11T09:23:04+09:00",
            "GSI_3_SK": 0,
            "user_id": "test_user_id_1",
            "user_name": "問屋町　花子",
            "department": "ＩＴＳ事業部",
            "job_type": "管理職",
            "age_range": "50",
            "updated_at": "2022-04-11T09:23:04+09:00",
            "post_review_count": 0,
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "user#test_user_id_2",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-05-02T16:43:25+09:00",
            "GSI_3_SK": 0,
            "user_id": "test_user_id_2",
            "user_name": "北ノ庄　肇",
            "department": "金融システム事業部",
            "job_type": "営業職",
            "age_range": "30",
            "updated_at": "2022-05-02T16:43:25+09:00",
            "post_review_count": 0,
        }

        self.table.put_item(Item=item)

        user_repository = UserRepository()

        users = user_repository.get_all()

        assert len(users) == 3

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

        assert users[2]["user_id"] == "test_user_id_2"
        assert users[2]["user_name"] == "北ノ庄　肇"
        assert users[2]["department"] == "金融システム事業部"
        assert users[2]["job_type"] == "営業職"
        assert users[2]["age_range"] == "30"
        assert users[2]["updated_at"] == "2022-05-02T16:43:25+09:00"

    def test_ユーザー情報が0件の場合に空のListを返すこと(self):
        # DBが空であることを確認
        response = self.table.scan()
        assert len(response["Items"]) == 0

        user_repository = UserRepository()
        users = user_repository.get_all()

        assert len(users) == 0

    def test_レビューを投稿したユーザを取得できること(self):
        item = {
            "PK": "user#test_user_id_0",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_3_SK": 1,
            "user_id": "test_user_id_0",
            "user_name": "永和　太郎",
            "department": "ＩＴＳ事業部",
            "job_type": "技術職",
            "age_range": "20",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "post_review_count": 1,
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "user#test_user_id_1",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-04-11T09:23:04+09:00",
            "GSI_3_SK": 2,
            "user_id": "test_user_id_1",
            "user_name": "問屋町　花子",
            "department": "ＩＴＳ事業部",
            "job_type": "管理職",
            "age_range": "50",
            "updated_at": "2022-04-11T09:23:04+09:00",
            "post_review_count": 2,
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "user#test_user_id_2",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-05-02T16:43:25+09:00",
            "GSI_3_SK": 0,
            "user_id": "test_user_id_2",
            "user_name": "北ノ庄　肇",
            "department": "金融システム事業部",
            "job_type": "営業職",
            "age_range": "30",
            "updated_at": "2022-05-02T16:43:25+09:00",
            "post_review_count": 0,
        }

        self.table.put_item(Item=item)

        user_repository = UserRepository()

        users = user_repository.get_by_posted_review()

        assert len(users) == 2

        # レビュー投稿数が多い順でソート済み

        assert users[0]["user_id"] == "test_user_id_1"
        assert users[0]["user_name"] == "問屋町　花子"
        assert users[0]["department"] == "ＩＴＳ事業部"
        assert users[0]["job_type"] == "管理職"
        assert users[0]["age_range"] == "50"
        assert users[0]["updated_at"] == "2022-04-11T09:23:04+09:00"
        assert users[0]["post_review_count"] == 2

        assert users[1]["user_id"] == "test_user_id_0"
        assert users[1]["user_name"] == "永和　太郎"
        assert users[1]["department"] == "ＩＴＳ事業部"
        assert users[1]["job_type"] == "技術職"
        assert users[1]["age_range"] == "20"
        assert users[1]["updated_at"] == "2022-04-01T00:00:00+09:00"
        assert users[1]["post_review_count"] == 1

    def test_レビューを投稿したユーザが0件の場合に空配列を返すこと(self):
        item = {
            "PK": "user#test_user_id_0",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_3_SK": 0,
            "user_id": "test_user_id_0",
            "user_name": "永和　太郎",
            "department": "ＩＴＳ事業部",
            "job_type": "技術職",
            "age_range": "20",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "post_review_count": 0,
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "user#test_user_id_1",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-04-11T09:23:04+09:00",
            "GSI_3_SK": 0,
            "user_id": "test_user_id_1",
            "user_name": "問屋町　花子",
            "department": "ＩＴＳ事業部",
            "job_type": "管理職",
            "age_range": "50",
            "updated_at": "2022-04-11T09:23:04+09:00",
            "post_review_count": 0,
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "user#test_user_id_2",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-05-02T16:43:25+09:00",
            "GSI_3_SK": 0,
            "user_id": "test_user_id_2",
            "user_name": "北ノ庄　肇",
            "department": "金融システム事業部",
            "job_type": "営業職",
            "age_range": "30",
            "updated_at": "2022-05-02T16:43:25+09:00",
            "post_review_count": 0,
        }

        self.table.put_item(Item=item)

        user_repository = UserRepository()

        users = user_repository.get_by_posted_review()

        assert len(users) == 0
        assert isinstance(users, list)

    def test_初期状態から最初のユーザー情報を作成できること(self):
        item = self.table.get_item(Key={"PK": "user#test_user_id"}).get("Item")

        assert item is None

        user_repository = UserRepository()

        user_repository.create(
            {
                "user_id": "test_user_id",
                "user_name": "永和　太郎",
                "department": "ＩＴＳ事業部",
                "job_type": "技術職",
                "age_range": "20",
                "updated_at": "2022-04-01T00:00:00+09:00",
                "post_review_count": 0,
            }
        )

        actual = self.table.get_item(Key={"PK": "user#test_user_id"}).get("Item")

        assert actual["PK"] == "user#test_user_id"
        assert actual["GSI_PK"] == "user"
        assert actual["GSI_0_SK"] == "2022-04-01T00:00:00+09:00"
        assert actual["GSI_3_SK"] == 0
        assert actual["user_id"] == "test_user_id"
        assert actual["user_name"] == "永和　太郎"
        assert actual["department"] == "ＩＴＳ事業部"
        assert actual["job_type"] == "技術職"
        assert actual["age_range"] == "20"
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"
        assert actual["post_review_count"] == 0

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
                "post_review_count": 0,
            }
        )

        actual = self.table.get_item(Key={"PK": "user#test_user_id"}).get("Item")

        assert actual["PK"] == "user#test_user_id"
        assert actual["GSI_PK"] == "user"
        assert actual["GSI_0_SK"] == "2022-04-15T09:20:12+09:00"
        assert actual["GSI_3_SK"] == 0
        assert actual["user_id"] == "test_user_id"
        assert actual["user_name"] == "永和 花子"
        assert actual["department"] == "金融システム事業部"
        assert actual["job_type"] == "営業職"
        assert actual["age_range"] == "30"
        assert actual["updated_at"] == "2022-04-15T09:20:12+09:00"
        assert actual["post_review_count"] == 0

        user_repository.create(
            {
                "user_id": "test_user_id",
                "user_name": "上書き次郎",
                "department": "金融システム事業部",
                "job_type": "管理職",
                "age_range": "50",
                "updated_at": "2022-04-28T09:32:14+09:00",
                "post_review_count": 0,
            }
        )

        actual = self.table.get_item(Key={"PK": "user#test_user_id"}).get("Item")

        assert actual["PK"] == "user#test_user_id"
        assert actual["GSI_PK"] == "user"
        assert actual["GSI_0_SK"] == "2022-04-28T09:32:14+09:00"
        assert actual["GSI_3_SK"] == 0
        assert actual["user_id"] == "test_user_id"
        assert actual["user_name"] == "上書き次郎"
        assert actual["department"] == "金融システム事業部"
        assert actual["job_type"] == "管理職"
        assert actual["age_range"] == "50"
        assert actual["updated_at"] == "2022-04-28T09:32:14+09:00"
        assert actual["post_review_count"] == 0

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
                "post_review_count": 0,
            }
        )

        actual = self.table.get_item(Key={"PK": "user#test_user_id"}).get("Item")

        assert actual["PK"] == "user#test_user_id"
        assert actual["GSI_PK"] == "user"
        assert actual["GSI_0_SK"] == "2022-04-15T09:20:12+09:00"
        assert actual["GSI_3_SK"] == 0
        assert actual["user_id"] == "test_user_id"
        assert actual["user_name"] == "永和 花子"
        assert actual["department"] == "金融システム事業部"
        assert actual["job_type"] == "営業職"
        assert actual["age_range"] == "30"
        assert actual["updated_at"] == "2022-04-15T09:20:12+09:00"
        assert actual["post_review_count"] == 0

        user_repository.create(
            {
                "user_id": "test_user_id_1",
                "user_name": "追加　小次郎",
                "department": "金融システム事業部",
                "job_type": "技術職",
                "age_range": "40",
                "updated_at": "2022-04-28T09:32:14+09:00",
                "post_review_count": 0,
            }
        )

        actual = self.table.get_item(Key={"PK": "user#test_user_id_1"}).get("Item")

        assert actual["PK"] == "user#test_user_id_1"
        assert actual["GSI_PK"] == "user"
        assert actual["GSI_0_SK"] == "2022-04-28T09:32:14+09:00"
        assert actual["GSI_3_SK"] == 0
        assert actual["user_id"] == "test_user_id_1"
        assert actual["user_name"] == "追加　小次郎"
        assert actual["department"] == "金融システム事業部"
        assert actual["job_type"] == "技術職"
        assert actual["age_range"] == "40"
        assert actual["updated_at"] == "2022-04-28T09:32:14+09:00"
        assert actual["post_review_count"] == 0

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
                "post_review_count": 0,
            }
        )

        actual = self.table.get_item(Key={"PK": "user#test_user_id"}).get("Item")

        assert actual["PK"] == "user#test_user_id"
        assert actual["GSI_PK"] == "user"
        assert actual["GSI_0_SK"] == "2022-04-15T09:20:12+09:00"
        assert actual["GSI_3_SK"] == 0
        assert actual["user_id"] == "test_user_id"
        assert actual["user_name"] == "永和 花子"
        assert actual["department"] == "金融システム事業部"
        assert actual["job_type"] == "営業職"
        assert actual["age_range"] == "30"
        assert actual["updated_at"] == "2022-04-15T09:20:12+09:00"
        assert actual["post_review_count"] == 0

        user_repository.create(
            {
                "user_id": "test_user_id_1",
                "user_name": "永和 花子",
                "department": "金融システム事業部",
                "job_type": "営業職",
                "age_range": "30",
                "updated_at": "2022-04-15T09:20:12+09:00",
                "post_review_count": 0,
            }
        )

        actual = self.table.get_item(Key={"PK": "user#test_user_id_1"}).get("Item")

        assert actual["PK"] == "user#test_user_id_1"
        assert actual["GSI_PK"] == "user"
        assert actual["GSI_0_SK"] == "2022-04-15T09:20:12+09:00"
        assert actual["GSI_3_SK"] == 0
        assert actual["user_id"] == "test_user_id_1"
        assert actual["user_name"] == "永和 花子"
        assert actual["department"] == "金融システム事業部"
        assert actual["job_type"] == "営業職"
        assert actual["age_range"] == "30"
        assert actual["updated_at"] == "2022-04-15T09:20:12+09:00"
        assert actual["post_review_count"] == 0

    def test_投稿したレビューの数を更新できること(self):
        item = {
            "PK": "user#test_user_id_0",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_3_SK": 1,
            "user_id": "test_user_id_0",
            "user_name": "永和　太郎",
            "department": "ＩＴＳ事業部",
            "job_type": "技術職",
            "age_range": "20",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "post_review_count": 1,
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "user#test_user_id_1",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-04-11T09:23:04+09:00",
            "GSI_3_SK": 0,
            "user_id": "test_user_id_1",
            "user_name": "問屋町　花子",
            "department": "ＩＴＳ事業部",
            "job_type": "管理職",
            "age_range": "50",
            "updated_at": "2022-04-11T09:23:04+09:00",
            "post_review_count": 0,
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "user#test_user_id_2",
            "GSI_PK": "user",
            "GSI_0_SK": "2022-05-02T16:43:25+09:00",
            "GSI_3_SK": 0,
            "user_id": "test_user_id_2",
            "user_name": "北ノ庄　肇",
            "department": "金融システム事業部",
            "job_type": "営業職",
            "age_range": "30",
            "updated_at": "2022-05-02T16:43:25+09:00",
            "post_review_count": 0,
        }

        self.table.put_item(Item=item)

        actual = self.table.get_item(Key={"PK": "user#test_user_id_1"}).get("Item")

        assert actual["GSI_3_SK"] == 0
        assert actual["post_review_count"] == 0

        user_repository = UserRepository()

        user_repository.update_post_review_count(user_id="test_user_id_1", count=1)

        actual = self.table.get_item(Key={"PK": "user#test_user_id_1"}).get("Item")

        assert actual["GSI_3_SK"] == 1
        assert actual["post_review_count"] == 1
