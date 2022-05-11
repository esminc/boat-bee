import datetime
from typing import Any, Optional, TypedDict

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.repository.book_review import BookReview

book_review_repository = BookReview()


class GetConditions(TypedDict):
    score_for_me: Optional[str]
    score_for_others: Optional[str]


def get_reviews(
    logger: Any, conditions: Optional[GetConditions] = None
) -> Optional[list[ReviewContents]]:
    try:
        return book_review_repository.get(conditions)

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
                "book_image_url": review_contents["book_image_url"],
                "book_author": review_contents["book_author"],
                "book_url": review_contents["book_url"],
            }
        )

    except Exception as error:  # pylint: disable=broad-except
        logger.exception(f"Failed to store data {error}")
