# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name


from moto import mock_dynamodb  # type: ignore

from bee_slack_app.model.user_action import UserAction
from bee_slack_app.repository.database import create_table
from bee_slack_app.repository.user_action_repository import UserActionRepository


@mock_dynamodb
class TestUserActionRepository:
    def setup_method(self, _):
        self.table = create_table()

    def test_ユーザの行動履歴を保存できること(self):

        item = self.table.get_item(
            Key={"PK": "user_action#dummy_user_id_0#2022-04-01T00:00:00+09:00"}
        ).get("Item")

        assert item is None

        item = self.table.get_item(
            Key={"PK": "user_action#dummy_user_id_1#2022-04-02T00:00:00+09:00"}
        ).get("Item")

        assert item is None

        user_action_repository = UserActionRepository()

        item: UserAction = {
            "user_id": "dummy_user_id_0",
            "created_at": "2022-04-01T00:00:00+09:00",
            "action_name": "dummy_action_name_0",
            "status": "dummy_status_0",
            "payload": None,
        }

        user_action_repository.put(item)

        item: UserAction = {
            "user_id": "dummy_user_id_1",
            "created_at": "2022-04-02T00:00:00+09:00",
            "action_name": "dummy_action_name_1",
            "status": "dummy_status_1",
            "payload": {"dummy_key": "dummy_value"},
        }

        user_action_repository.put(item)

        actual = self.table.get_item(
            Key={
                "PK": "user_action#dummy_user_id_0#2022-04-01T00:00:00+09:00",
            }
        )["Item"]

        assert actual["PK"] == "user_action#dummy_user_id_0#2022-04-01T00:00:00+09:00"
        assert actual["GSI_PK"] == "user_action"
        assert actual["GSI_0_SK"] == "2022-04-01T00:00:00+09:00"
        assert actual["GSI_1_SK"] == "dummy_user_id_0"
        assert actual["user_id"] == "dummy_user_id_0"
        assert actual["created_at"] == "2022-04-01T00:00:00+09:00"
        assert actual["action_name"] == "dummy_action_name_0"
        assert actual["status"] == "dummy_status_0"
        assert actual["payload"] is None

        actual = self.table.get_item(
            Key={
                "PK": "user_action#dummy_user_id_1#2022-04-02T00:00:00+09:00",
            }
        )["Item"]

        assert actual["PK"] == "user_action#dummy_user_id_1#2022-04-02T00:00:00+09:00"
        assert actual["GSI_PK"] == "user_action"
        assert actual["GSI_0_SK"] == "2022-04-02T00:00:00+09:00"
        assert actual["GSI_1_SK"] == "dummy_user_id_1"
        assert actual["user_id"] == "dummy_user_id_1"
        assert actual["created_at"] == "2022-04-02T00:00:00+09:00"
        assert actual["action_name"] == "dummy_action_name_1"
        assert actual["status"] == "dummy_status_1"
        assert actual["payload"] == {"dummy_key": "dummy_value"}
