import os

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.repository.database import get_database_client


# This is a sample
class BookReview:
    def __init__(self):
        self.table = get_database_client().Table(os.environ["DYNAMODB_TABLE"])

    def get_all(self) -> list[ReviewContents]:
        """
        本のレビューを全件取得する

        Returns:
            list[ReviewContents]: 本のレビューのリスト
        """
        response = self.table.scan()
        items = response["Items"]

        # レスポンスに LastEvaluatedKey が含まれなくなるまでループ処理を実行する
        # see https://dev.classmethod.jp/articles/hot-to-get-more-than-1mb-of-data-from-dynamodb-when-using-scan/
        while "LastEvaluatedKey" in response:
            response = self.table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            items.extend(response["Items"])

        return items

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
