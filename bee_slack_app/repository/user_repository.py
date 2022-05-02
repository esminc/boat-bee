"""ユーザー情報の追加・更新・削除を行います
"""
import os

from bee_slack_app.model.user import User
from bee_slack_app.repository.database import get_database_client


class UserRepository:
    def __init__(self):
        self.table = get_database_client().Table(os.environ["DYNAMODB_TABLE"] + "-user")

    def get_user(self, user_id: str) -> list[User]:
        """
        自分のユーザー情報を取得する

        Returns:
                    list[User]: 自分のユーザー情報のリスト
        """
        response = self.table.get_item(key={"user_id": user_id})

        return response["Item"]

    def create(self, user: User) -> None:
        # 未実装
        pass
