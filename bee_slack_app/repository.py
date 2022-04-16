import os

import boto3  # type: ignore

# dynamodb = boto3.resource("dynamodb")
# dynamodb = boto3.resource('dynamodb',endpoint_url='http://localhost:8000')

# This is a sample
class _BookReview:
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    # dynamodb = boto3.resource('dynamodb',endpoint_url='http://localhost:8000')
    table = dynamodb.Table("dee-dev")

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


# bookReview = _BookReview()


def update():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    # dynamodb = boto3.resource('dynamodb',endpoint_url='http://localhost:8000')
    table = dynamodb.Table("dee-dev")

    item = {
        "userId": "test-id",
        "review_text": "This is a sample text.",
    }

    table.put_item(Item=item)

    return item
