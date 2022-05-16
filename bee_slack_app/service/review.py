from typing import Any, Optional, TypedDict, Union

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.repository.book_review import BookReview
from bee_slack_app.utils import datetime

book_review_repository = BookReview()


class GetConditions(TypedDict):
    score_for_me: Optional[str]
    score_for_others: Optional[str]


class ReviewItemKey(TypedDict):
    user_id: str
    isbn: str


class GetResponse(TypedDict):
    items: list[ReviewContents]
    keys: list[Union[ReviewItemKey, str]]


def get_reviews(
    *,
    logger: Any,
    conditions: Optional[GetConditions] = None,
    limit: int,
    keys: list[ReviewItemKey],
) -> Optional[GetResponse]:
    """
    次のlimit分のレビューを取得する

    Returns
        items: 取得したレビューのリスト
        keys: 更新された読み込みキーのリスト。これ以上アイテムが存在しない場合は、リストの最後の要素が"end"となる。
    """
    try:

        start_key = keys[-1] if len(keys) > 0 else None

        reviews = book_review_repository.get(
            conditions=conditions, limit=limit, start_key=start_key
        )

        last_key = [reviews["last_key"]] if reviews["last_key"] else ["end"]  # type: ignore

        return {"items": reviews["items"], "keys": keys + last_key}  # type: ignore

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def get_reviews_before(
    *,
    logger: Any,
    conditions: Optional[GetConditions] = None,
    limit: int,
    keys: list[ReviewItemKey],
) -> Optional[GetResponse]:
    """
    前のlimit分のレビューを取得する

    Returns
        items: 取得したレビューのリスト
        keys: 更新された読み込みキーのリスト
    """
    try:
        is_move_to_first = len(keys) < 3

        start_key = None if is_move_to_first else keys[-3]

        reviews = book_review_repository.get(
            conditions=conditions, limit=limit, start_key=start_key
        )

        return {
            "items": reviews["items"],
            "keys": [reviews["last_key"]] if is_move_to_first else keys[:-1],  # type: ignore
        }

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
                "updated_at": datetime.now(),
                "book_image_url": review_contents["book_image_url"],
                "book_author": review_contents["book_author"],
                "book_url": review_contents["book_url"],
            }
        )

    except Exception as error:  # pylint: disable=broad-except
        logger.exception(f"Failed to store data {error}")
