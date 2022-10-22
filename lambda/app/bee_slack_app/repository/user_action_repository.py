from bee_slack_app.model import UserAction
from bee_slack_app.repository import database

GSI_PK_VALUE = "user_action"


def _encode_partition_key(*, user_id: str, created_at: str) -> str:
    return f"user_action#{user_id}#{created_at}"


class UserActionRepository:  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.table = database.get_table()

    def put(self, user_action: UserAction) -> None:
        partition_key = _encode_partition_key(
            user_id=user_action["user_id"], created_at=user_action["created_at"]
        )

        item = {
            database.PK: partition_key,
            database.GSI_PK: GSI_PK_VALUE,
            database.GSI_0_SK: user_action["created_at"],
            database.GSI_1_SK: user_action["user_id"],
            "user_id": user_action["user_id"],
            "created_at": user_action["created_at"],
            "action_name": user_action["action_name"],
            "status": user_action["status"],
            "payload": user_action["payload"],
        }

        self.table.put_item(Item=item)
