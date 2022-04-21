import os

from bee_slack_app.repository.database import dynamodb


# This is a sample
class BookReview:
    def __init__(self):

        self.table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    def create(self, review):
        item = {
            "user_id": review["user_id"],
            "book_title": review["book_title"],
            "isbn": review["isbn"],
            "score_for_me": review["score_for_me"],
            "score_for_others": review["score_for_others"],
            "review_comment": review["review_comment"],
            "updated_at": review["updated_at"],
        }

        self.table.put_item(Item=item)

        return item

    def delete(self):
        # 未実装
        pass
