from logging import getLogger
from typing import Optional

from injector import Injector, inject

from bee_slack_app.model.user import User
from bee_slack_app.repository.user_repository import UserRepository
from bee_slack_app.utils import datetime


class UserService:
    @inject
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    def get_user(self, user_id: str) -> Optional[User]:
        """
        ユーザ情報を取得する

        Args:
            user_id : 取得するユーザー情報のuser_id。

        Returns:
            User: 取得したユーザー情報。未登録の場合は、Noneが返る。
        """
        logger = getLogger(__name__)

        try:
            return self.user_repository.get(user_id)

        except Exception:  # pylint: disable=broad-except
            logger.exception("Failed to get data.")
            return None

    def get_all_user(self) -> list[User]:
        """
        ユーザ情報を取得する


        Returns:
            User: 取得したユーザー情報。未登録の場合は、空のリストが返る。
        """
        logger = getLogger(__name__)

        try:
            return self.user_repository.get_all()

        except Exception:  # pylint: disable=broad-except
            logger.exception("Failed to get data.")
            return []

    def add_user(self, user: User) -> None:
        """
        ユーザ情報の登録・更新をする
        """
        logger = getLogger(__name__)

        try:
            self.user_repository.create(
                {
                    "user_id": user["user_id"],
                    "user_name": user["user_name"],
                    "department": user["department"],
                    "job_type": user["job_type"],
                    "age_range": user["age_range"],
                    "updated_at": datetime.now(),
                }
            )

        except Exception as error:  # pylint: disable=broad-except
            logger.exception(f"Failed to store data {error}")


user_service = Injector().get(UserService)
