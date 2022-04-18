import datetime
from typing import Any

from bee_slack_app.repository.book_review import book_review_repository  # type: ignore


def post_review(
    logger: Any,
    user_id: str,
    book_title: str,
    isbn: str,
    score_for_me: int,
    score_for_others: int,
    review_comment: str,
) -> None:
    # 入力されたデータを使った処理を実行。このサンプルでは DB に保存する処理を行う

    try:
        # DB に保存
        book_review_repository.create(
            {
                "user_id": user_id,
                "book_title": book_title,
                "isbn": isbn,
                "score_for_me": score_for_me,
                "score_for_others": score_for_others,
                "review_comment": review_comment,
                "updated_at": datetime.datetime.now(
                    datetime.timezone(datetime.timedelta(hours=9))
                ).isoformat(timespec="seconds"),
            }
        )

    except Exception as error:  # pylint: disable=broad-except
        # エラーをハンドリング
        logger.exception(f"Failed to store data {error}")
