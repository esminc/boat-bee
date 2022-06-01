from logging import getLogger
from typing import Any

from injector import Injector, inject

from bee_slack_app.model.user_action import UserAction
from bee_slack_app.repository.user_action_repository import UserActionRepository
from bee_slack_app.utils import datetime


class UserActionService:
    @inject
    def __init__(
        self,
        user_action_repository: UserActionRepository,
    ):
        self.user_action_repository = user_action_repository

    def record_user_action(
        self, *, user_id: str, action_name: str, status: str = "ok", payload: Any = None
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

            self.user_action_repository.put(item)

        except Exception:  # pylint: disable=broad-except
            logger.exception("Failed to put data.")


user_action_service = Injector().get(UserActionService)
