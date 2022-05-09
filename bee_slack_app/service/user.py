# pylint: disable=duplicate-code
import datetime
from typing import Any, Optional

from bee_slack_app.model.user import User
from bee_slack_app.repository.user_repository import UserRepository

user_repository = UserRepository()


def get_user(logger: Any, user_id: str) -> Optional[User]:
    try:
        return user_repository.get(user_id)

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def add_user(logger: Any, user: User) -> None:
    """
    ユーザ情報の登録・更新をする
    """

    try:
        user_repository.create(
            {
                "user_id": user["user_id"],
                "user_name": user["user_name"],
                "department": user["department"],
                "job_type": user["job_type"],
                "age_range": user["age_range"],
                "updated_at": datetime.datetime.now(
                    datetime.timezone(datetime.timedelta(hours=9))
                ).isoformat(timespec="seconds"),
            }
        )

    except Exception as error:  # pylint: disable=broad-except
        logger.exception(f"Failed to store data {error}")
