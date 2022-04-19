import os

import boto3  # type: ignore

dynamodb = boto3.resource("dynamodb")


# This is a sample
class _BookReview:
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

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


book_review_repository = _BookReview()
