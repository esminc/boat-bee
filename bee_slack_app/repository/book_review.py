import os

import boto3  # type: ignore


# This is a sample
class BookReview:
    def __init__(self):
        # 環境変数にDYNAMODB_ENDPOINTが設定されていればそこに接続する（ローカル環境）
        # 設定されていなければデフォルトのDynamoDBに接続する（AWSの環境）
        # TODO: この処理はアプリ全体で共通のため1か所に集めたい
        endpoint_url = os.getenv("DYNAMODB_ENDPOINT", None)
        dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
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
