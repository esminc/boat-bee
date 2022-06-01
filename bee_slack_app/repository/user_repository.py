"""ユーザー情報の追加・更新・削除を行います
"""
import os
from typing import Optional

from boto3.dynamodb.conditions import Key  # type: ignore
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

        items = self.table.query(
            KeyConditionExpression=Key("user_id").eq(user_id),
        )["Items"]

        if not items:
            return None

        user = {
            item["user_attribute_key"]: item["user_attribute_value"] for item in items
        }

        user["user_id"] = user_id

        return user

    def get_all(self) -> list[User]:
        """
        全てのユーザー情報を取得する

        Returns:
            list[User]: 取得した全てユーザー情報のリスト。未登録の場合は、空のリストを返す
        """
        items = self.table.scan()["Items"]

        users = {}

        for item in items:
            user_id = item["user_id"]

            user = users.get(user_id)
            if not user:
                users[user_id] = {}
                user = users.get(user_id)

            user_attribute_key = item["user_attribute_key"]
            user[user_attribute_key] = item["user_attribute_value"]

        return [{"user_id": k, **v} for k, v in users.items()]

    def get_by_posted_review(self) -> list[User]:
        """
        レビューを投稿しているユーザを取得する
        """

        items = self.table.query(
            IndexName="UserTableGSI0",
            KeyConditionExpression=Key("user_attribute_value").eq("post_review_true"),
        )["Items"]

        users = [self.get(item["user_id"]) for item in items]

        return users

    def update_posted_review(self, *, user_id: str, posted_review: bool):
        """
        レビューを投稿しているか、を更新する
        """
        user_attribute_value = (
            "post_review_true" if posted_review else "post_review_false"
        )

        self.table.put_item(
            Item={
                "user_id": user_id,
                "user_attribute_key": "post_review",
                "user_attribute_value": user_attribute_value,
            }
        )

    def create(self, user: User) -> None:
        """
        データを追加および上書きします
        """
        item = {
            "user_name": user["user_name"],
            "department": user["department"],
            "job_type": user["job_type"],
            "age_range": user["age_range"],
            "updated_at": user["updated_at"],
        }

        for k, v in item.items():
            self.table.put_item(
                Item={
                    "user_id": user["user_id"],
                    "user_attribute_key": k,
                    "user_attribute_value": v,
                }
            )

    def delete(self):
        """
        データを削除します
        """
        # 未実装
