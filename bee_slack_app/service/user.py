import datetime
import logging
from typing import Any, Optional

from bee_slack_app.model.user import User
from bee_slack_app.repository.user_profile import UserProfile

user_profile_repository = UserProfile()


def add_user(user_contents: User) -> None:
    # 入力されたデータを使った処理を実行。このサンプルでは DB に保存する処理を行う

    try:
        # DB に保存
        user_profile_repository.create(
            {
                "user_id": user_contents["user_id"],
                "book_title": user_contents["user_name"],
                "isbn": user_contents["department"],
                "score_for_me": user_contents["job_type"],
                "score_for_others": user_contents["age_range"],
                "updated_at": datetime.datetime.now(
                    datetime.timezone(datetime.timedelta(hours=9))
                ).isoformat(timespec="seconds"),
            }
        )

    except Exception as error:  # pylint: disable=broad-except
        # エラーをハンドリング
        logger.exception(f"Failed to store data {error}")
