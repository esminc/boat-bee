"""ユーザー情報の追加・更新・削除を行います
"""
from typing import Optional

from boto3.dynamodb.conditions import Key  # type: ignore

from bee_slack_app.model.user import User
from bee_slack_app.repository import database

GSI_PK_VALUE = "user"


def _encode_partition_key(*, user_id: str) -> str:
    return f"user#{user_id}"


class UserRepository:
    def __init__(self):
        self.table = database.get_table()

    def get(self, user_id: str) -> Optional[User]:
        """
        自分のユーザー情報を取得する

        Args:
            user_id : 検索するユーザー情報のuser_id

        Returns:
            User: 取得したユーザー情報。未登録の場合は、Noneを返します。
        """
        partition_key = _encode_partition_key(user_id=user_id)
        return self.table.get_item(Key={database.PK: partition_key}).get("Item")

    def get_all(self) -> list[User]:
        """
        全てのユーザー情報を取得する

        Returns:
            list[User]: 取得した全てユーザー情報のリスト。未登録の場合は、空のリストを返す
        """
        return self.table.query(
            IndexName=database.GSI_0,
            KeyConditionExpression=Key(database.GSI_PK).eq(GSI_PK_VALUE),
        )["Items"]

    def create(self, user: User) -> None:
        """
        データを追加および上書きします
        """
        partition_key = _encode_partition_key(user_id=user["user_id"])

        item = {
            database.PK: partition_key,
            database.GSI_PK: GSI_PK_VALUE,
            database.GSI_0_SK: user["updated_at"],
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
