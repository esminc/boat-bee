from logging import getLogger
from typing import Any

from bee_slack_app.model.user_action import UserAction
from bee_slack_app.repository.user_action_repository import UserActionRepository
from bee_slack_app.utils import datetime

user_action_repository = UserActionRepository()


def record_user_action(
    *, user_id: str, action_type: str, status: str = "ok", payload: Any = None
) -> None:
    """
    ユーザの行動履歴を保存する
    """

    try:
        logger = getLogger(__name__)

        item: UserAction = {
            "user_id": user_id,
            "created_at": datetime.now(),
            "action_type": action_type,
            "status": status,
            "payload": payload,
        }

        logger.info(item)

        user_action_repository.put(item)

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to put data.")
