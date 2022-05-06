"""ユーザー情報の追加・更新・削除を行います
"""
import os

from typing import Optional
from bee_slack_app.model.user import User
from bee_slack_app.repository.database import get_database_client


class UserRepository:
    def __init__(self):
        self.table = get_database_client().Table(os.environ["DYNAMODB_TABLE"] + "-user")

    def get(self, user_id: str) -> Optional[User]:
        """
        自分のユーザー情報を取得する

        Args:
            user_id : 検索するユーザー情報のuser_id

        Returns:
            User: 取得したユーザー情報。未登録の場合は、Noneを返します。
        """
        response = self.table.get_item(Key={"user_id": user_id})
        return response["Item"] if "Item" in response else None

    def create(self, user: Optional[User]) -> None:
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
