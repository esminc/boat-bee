import os

from bee_slack_app.model.user_action import UserAction
from bee_slack_app.repository.database import get_database_client


class UserActionRepository:  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.table = get_database_client().Table(
            os.environ["DYNAMODB_TABLE"] + "-user-action"
        )

    def put(self, item: UserAction) -> None:
        self.table.put_item(Item=item)
