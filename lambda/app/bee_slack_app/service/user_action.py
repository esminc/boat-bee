from logging import getLogger
from typing import Any

from bee_slack_app.model import UserAction
from bee_slack_app.repository import UserActionRepository
from bee_slack_app.utils import datetime

user_action_repository = UserActionRepository()


def record_user_action(
    *, user_id: str, action_name: str, status: str = "ok", payload: Any = None
) -> None:
    """
    ユーザの行動履歴を保存する
    """

    try:
        logger = getLogger(__name__)

        item: UserAction = {
            "user_id": user_id,
            "created_at": datetime.now(),
            "action_name": action_name,
            "status": status,
            "payload": payload,
        }

        logger.info(item)

        user_action_repository.put(item)

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to put data.")
