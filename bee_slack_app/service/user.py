import datetime
import logging
from typing import Any, Optional

from bee_slack_app.model.user import User
from bee_slack_app.repository.user_repository import UserRepository

user_repository = UserRepository()


def add_user(user: User) -> None:
    """
    ユーザ情報の登録・更新をする

    """

    try:
        user_repository.create(
            {
                "user_id": user["user_id"],
                "book_title": user["user_name"],
                "isbn": user["department"],
                "score_for_me": user["job_type"],
                "score_for_others": user["age_range"],
                "updated_at": datetime.datetime.now(
                    datetime.timezone(datetime.timedelta(hours=9))
                ).isoformat(timespec="seconds"),
            }
        )

    except Exception as error:  # pylint: disable=broad-except
        logger.exception(f"Failed to store data {error}")
