# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name
# pylint: disable=invalid-name


from moto import mock_dynamodb  # type: ignore

from bee_slack_app.repository import database
from bee_slack_app.repository.suggested_book_repository import SuggestedBookRepository


@mock_dynamodb
class TestSuggestedBookRepository:
    def setup_method(self, _):
        self.table = database.create_table()

    def test_DBの先頭にあるおすすめされた本を取得できること(self):
        item = {
            "PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0",
            "GSI_PK": "suggested_book",
            "GSI_0_SK": "test_user_id_0",
            "GSI_1_SK": "1234567890123",
            "GSI_2_SK": "dummy_ml_model_0",
            "user_id": "test_user_id_0",
            "isbn": "1234567890123",
            "ml_model": "dummy_ml_model_0",
            "interested": True,
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "suggested_book#test_user_id_1#9234567890123#dummy_ml_model_1",
            "GSI_PK": "suggested_book",
            "GSI_0_SK": "test_user_id_1",
            "GSI_1_SK": "9234567890123",
            "GSI_2_SK": "dummy_ml_model_1",
            "user_id": "test_user_id_1",
            "isbn": "1234567890123",
            "ml_model": "dummy_ml_model_1",
            "interested": True,
            "updated_at": "2022-04-11T09:23:04+09:00",
        }

        self.table.put_item(Item=item)

        suggested_book_repository = SuggestedBookRepository()

        suggested_book = suggested_book_repository.get(
            user_id="test_user_id_0", isbn="1234567890123", ml_model="dummy_ml_model_0"
        )

        assert suggested_book["user_id"] == "test_user_id_0"
        assert suggested_book["isbn"] == "1234567890123"
        assert suggested_book["ml_model"] == "dummy_ml_model_0"
        assert suggested_book["interested"] is True
        assert suggested_book["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_DBの最後尾にあるおすすめされた本を取得できること(self):
        item = {
            "PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0",
            "GSI_PK": "suggested_book",
            "GSI_0_SK": "test_user_id_0",
            "GSI_1_SK": "1234567890123",
            "GSI_2_SK": "dummy_ml_model_0",
            "user_id": "test_user_id_0",
            "isbn": "1234567890123",
            "ml_model": "dummy_ml_model_0",
            "interested": True,
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "suggested_book#test_user_id_1#9234567890123#dummy_ml_model_1",
            "GSI_PK": "suggested_book",
            "GSI_0_SK": "test_user_id_1",
            "GSI_1_SK": "9234567890123",
            "GSI_2_SK": "dummy_ml_model_1",
            "user_id": "test_user_id_1",
            "isbn": "9234567890123",
            "ml_model": "dummy_ml_model_1",
            "interested": False,
            "updated_at": "2022-04-11T09:23:04+09:00",
        }

        self.table.put_item(Item=item)

        suggested_book_repository = SuggestedBookRepository()

        suggested_book = suggested_book_repository.get(
            user_id="test_user_id_1", isbn="9234567890123", ml_model="dummy_ml_model_1"
        )

        assert suggested_book["user_id"] == "test_user_id_1"
        assert suggested_book["isbn"] == "9234567890123"
        assert suggested_book["ml_model"] == "dummy_ml_model_1"
        assert suggested_book["interested"] is False
        assert suggested_book["updated_at"] == "2022-04-11T09:23:04+09:00"

    def test_おすすめされた本が無い場合にNoneが返ること(self):
        item = {
            "PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0",
            "GSI_PK": "suggested_book",
            "GSI_0_SK": "test_user_id_0",
            "GSI_1_SK": "1234567890123",
            "GSI_2_SK": "dummy_ml_model_0",
            "user_id": "test_user_id_0",
            "isbn": "1234567890123",
            "ml_model": "dummy_ml_model_0",
            "interested": True,
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "suggested_book#test_user_id_1#9234567890123#dummy_ml_model_1",
            "GSI_PK": "suggested_book",
            "GSI_0_SK": "test_user_id_1",
            "GSI_1_SK": "9234567890123",
            "GSI_2_SK": "dummy_ml_model_1",
            "user_id": "test_user_id_1",
            "isbn": "1234567890123",
            "ml_model": "dummy_ml_model_1",
            "interested": False,
            "updated_at": "2022-04-11T09:23:04+09:00",
        }

        self.table.put_item(Item=item)

        suggested_book_repository = SuggestedBookRepository()

        suggested_book = suggested_book_repository.get(
            user_id="test_user_id_0", isbn="9234567890123", ml_model="dummy_ml_model_1"
        )

        assert suggested_book is None

    def test_おすすめされた本の情報を作成できること(self):
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert actual is None

        suggested_book_repository = SuggestedBookRepository()

        suggested_book_repository.create(
            {
                "user_id": "test_user_id_0",
                "isbn": "1234567890123",
                "ml_model": "dummy_ml_model_0",
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )

        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_ユーザーが同じでisbnとmlが異なるおすすめされた本を追加できること(self):
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert actual is None

        suggested_book_repository = SuggestedBookRepository()

        # １件目のテストデータを作成
        suggested_book_repository.create(
            {
                "user_id": "test_user_id_0",
                "isbn": "1234567890123",
                "ml_model": "dummy_ml_model_0",
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )

        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

        # ２件目のテストデータを作成（user_idのみ同じ）
        suggested_book_repository.create(
            {
                "user_id": "test_user_id_0",
                "isbn": "9234567890123",
                "ml_model": "dummy_ml_model_1",
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#9234567890123#dummy_ml_model_1"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#9234567890123#dummy_ml_model_1"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "9234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_1"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "9234567890123"
        assert actual["ml_model"] == "dummy_ml_model_1"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_ユーザーとisbnが同じでmlが異なるおすすめされた本を追加できること(self):
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert actual is None

        suggested_book_repository = SuggestedBookRepository()

        # １件目のテストデータを作成
        suggested_book_repository.create(
            {
                "user_id": "test_user_id_0",
                "isbn": "1234567890123",
                "ml_model": "dummy_ml_model_0",
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

        # ２件目のテストデータを作成（user_idとisbnが同じ、mlが異なる）
        suggested_book_repository.create(
            {
                "user_id": "test_user_id_0",
                "isbn": "1234567890123",
                "ml_model": "dummy_ml_model_1",
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_1"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_1"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_1"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_1"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_ユーザーとisbnが異なるがmlが同じおすすめされた本を追加できること(self):
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert actual is None

        suggested_book_repository = SuggestedBookRepository()

        # １件目のテストデータを作成
        suggested_book_repository.create(
            {
                "user_id": "test_user_id_0",
                "isbn": "1234567890123",
                "ml_model": "dummy_ml_model_0",
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

        # ２件目のテストデータを作成（user_idとisbnが異なる。mlが同じ。）
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_1#9234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert actual is None

        suggested_book_repository.create(
            {
                "user_id": "test_user_id_1",
                "isbn": "9234567890123",
                "ml_model": "dummy_ml_model_0",
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_1#9234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_1#9234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_1"
        assert actual["GSI_1_SK"] == "9234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_1"
        assert actual["isbn"] == "9234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_ユーザーとmlが異なるがisbnが同じおすすめされた本を追加できること(self):
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert actual is None

        suggested_book_repository = SuggestedBookRepository()

        # １件目のテストデータを作成
        suggested_book_repository.create(
            {
                "user_id": "test_user_id_0",
                "isbn": "1234567890123",
                "ml_model": "dummy_ml_model_0",
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

        # ２件目のテストデータを作成（user_idとmlが異なる。isbnが同じ。）
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_1#1234567890123#dummy_ml_model_1"}
        ).get("Item")

        assert actual is None

        suggested_book_repository.create(
            {
                "user_id": "test_user_id_1",
                "isbn": "1234567890123",
                "ml_model": "dummy_ml_model_1",
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_1#1234567890123#dummy_ml_model_1"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_1#1234567890123#dummy_ml_model_1"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_1"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_1"
        assert actual["user_id"] == "test_user_id_1"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_1"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_ユーザーとisbnとmlが全て異なるおすすめされた本を追加できること(self):
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")
        assert actual is None

        suggested_book_repository = SuggestedBookRepository()

        # １件目のテストデータを作成
        suggested_book_repository.create(
            {
                "user_id": "test_user_id_0",
                "isbn": "1234567890123",
                "ml_model": "dummy_ml_model_0",
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

        # ２件目のテストデータを作成（user_idとisbnとmlが異なる。）
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_1#9234567890123#dummy_ml_model_1"}
        ).get("Item")
        assert actual is None

        suggested_book_repository.create(
            {
                "user_id": "test_user_id_1",
                "isbn": "9234567890123",
                "ml_model": "dummy_ml_model_1",
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_1#9234567890123#dummy_ml_model_1"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_1#9234567890123#dummy_ml_model_1"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_1"
        assert actual["GSI_1_SK"] == "9234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_1"
        assert actual["user_id"] == "test_user_id_1"
        assert actual["isbn"] == "9234567890123"
        assert actual["ml_model"] == "dummy_ml_model_1"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_おすすめされた本を上書きできること(self):
        suggested_book_repository = SuggestedBookRepository()

        # １件目のテストデータを作成
        suggested_book_repository.create(
            {
                "user_id": "test_user_id_0",
                "isbn": "1234567890123",
                "ml_model": "dummy_ml_model_0",
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        )
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is True
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"

        # １件目に上書きするテストデータを作成
        suggested_book_repository.create(
            {
                "user_id": "test_user_id_0",
                "isbn": "1234567890123",
                "ml_model": "dummy_ml_model_0",
                "interested": False,
                "updated_at": "2022-04-01T10:00:05+09:00",
            }
        )
        actual = self.table.get_item(
            Key={"PK": "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"}
        ).get("Item")

        assert (
            actual["PK"]
            == "suggested_book#test_user_id_0#1234567890123#dummy_ml_model_0"
        )
        assert actual["GSI_PK"] == "suggested_book"
        assert actual["GSI_0_SK"] == "test_user_id_0"
        assert actual["GSI_1_SK"] == "1234567890123"
        assert actual["GSI_2_SK"] == "dummy_ml_model_0"
        assert actual["user_id"] == "test_user_id_0"
        assert actual["isbn"] == "1234567890123"
        assert actual["ml_model"] == "dummy_ml_model_0"
        assert actual["interested"] is False
        assert actual["updated_at"] == "2022-04-01T10:00:05+09:00"
