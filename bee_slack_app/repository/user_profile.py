import os

from bee_slack_app.model.user import User
from bee_slack_app.repository.database import get_database_client


# This is a sample
class UserProfile:
    def __init__(self):
        self.table = get_database_client().Table(os.environ["DYNAMODB_TABLE"])

    def get_all(self):
        # 未実装
        pass

    def create(self, profile: User):
        item = {
            "user_id": profile["user_id"],
            "user_name": profile["user_name"],
            "department": profile["department"],
            "job_type": profile["job_type"],
            "age_range": profile["age_range"],
            "updated_at": profile["updated_at"],
        }

        self.table.put_item(Item=item)

        return item

    def delete(self):
        # 未実装
        pass
