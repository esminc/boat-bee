import datetime
from typing import Any, Optional

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.repository.book_review import BookReview

book_review_repository = BookReview()


def get_review_all(logger: Any) -> Optional[list[ReviewContents]]:
    try:
        return book_review_repository.get()

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def post_review(logger: Any, review_contents: ReviewContents) -> None:
    try:
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
        logger.exception(f"Failed to store data {error}")
