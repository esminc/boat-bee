import datetime
from typing import Any

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.repository.book_review import book_review_repository


def post_review(logger: Any, review_contents: ReviewContents) -> None:
    # 入力されたデータを使った処理を実行。このサンプルでは DB に保存する処理を行う

    try:
        # DB に保存
        book_review_repository.create(
            {
                "user_id": review_contents["user_id"],
                "book_title": review_contents["book_title"],
                "isbn": review_contents["isbn"],
                "score_for_me": review_contents["score_for_me"],
                "score_for_others": review_contents["score_for_others"],
                "review_comment": review_contents["review_comment"],
                "updated_at": datetime.datetime.now(
                    datetime.timezone(datetime.timedelta(hours=9))
                ).isoformat(timespec="seconds"),
            }
        )

    except Exception as error:  # pylint: disable=broad-except
        # エラーをハンドリング
        logger.exception(f"Failed to store data {error}")
