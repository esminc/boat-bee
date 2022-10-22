# pylint: disable=non-ascii-name


from bee_slack_app.repository.user_action_repository import UserActionRepository
from bee_slack_app.service.user_action import record_user_action
from bee_slack_app.utils import datetime


def test_ユーザの行動履歴を保存できること(mocker):

    mock_user_action_repository_put = mocker.patch.object(
        UserActionRepository,
        "put",
    )

    mocker.patch.object(datetime, "now").return_value = "2022-04-01T00:00:00+09:00"

    record_user_action(
        user_id="dummy_user_id",
        action_name="dummy_action_name",
        status="dummy_status",
        payload="dummy_payload",
    )

    mock_user_action_repository_put.assert_called_once_with(
        {
            "user_id": "dummy_user_id",
            "created_at": "2022-04-01T00:00:00+09:00",
            "action_name": "dummy_action_name",
            "status": "dummy_status",
            "payload": "dummy_payload",
        }
    )
