import os

import boto3  # type: ignore

dynamodb = boto3.resource("dynamodb")


# This is a sample
class _BookReview:
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    def create(self):
        item = {
            "userId": "test-id",
            "review_text": "This is a sample text.",
        }

        self.table.put_item(Item=item)

        return item

    def delete(self):
        # 未実装
        pass


bookReview = _BookReview()
