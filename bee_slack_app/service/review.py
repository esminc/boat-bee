from typing import Any, Optional, TypedDict

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.repository.book_review import BookReview
from bee_slack_app.repository.google_books import GoogleBooks
from bee_slack_app.utils import datetime

book_review_repository = BookReview()
google_books_repository = GoogleBooks()


class GetConditions(TypedDict):
    score_for_me: Optional[str]
    score_for_others: Optional[str]


def get_review(logger: Any, user_id: str, isbn: str) -> Optional[ReviewContents]:
    try:
        return book_review_repository.get({"user_id": user_id, "isbn": isbn})

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


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
        isbn = review_contents["isbn"]

        book = google_books_repository.search_book_by_isbn(isbn)

        if book is None:
            logger.info(f"Failed to fetch book data by ISBN. ISBN: {isbn}")

        book_review_repository.create(
            {
                "user_id": review_contents["user_id"],
                "book_title": review_contents["book_title"],
                "isbn": review_contents["isbn"],
                "score_for_me": review_contents["score_for_me"],
                "score_for_others": review_contents["score_for_others"],
                "review_comment": review_contents["review_comment"],
                "updated_at": datetime.now(),
                "image_url": book and book.get("image_url"),
            }
        )

    except Exception as error:  # pylint: disable=broad-except
        logger.exception(f"Failed to store data {error}")
