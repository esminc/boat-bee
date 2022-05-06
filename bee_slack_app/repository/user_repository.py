"""ユーザー情報の追加・更新・削除を行います
"""
import os

from bee_slack_app.model.user import User
from bee_slack_app.repository.database import get_database_client


class UserRepository:
    def __init__(self):
        self.table = get_database_client().Table(os.environ["DYNAMODB_TABLE"] + "-user")

    def create(self, user: User) -> None:
        """
        データを追加および上書きします
        """
        item = {
            "user_id": user["user_id"],
            "user_name": user["user_name"],
            "department": user["department"],
            "job_type": user["job_type"],
            "age_range": user["age_range"],
            "updated_at": user["updated_at"],
        }

        self.table.put_item(Item=item)

    def delete(self):
        """
        データを削除します
        """
        # 未実装
