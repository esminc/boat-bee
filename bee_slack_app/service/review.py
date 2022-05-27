from typing import Any, Optional, TypedDict, Union

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.repository.review_repository import ReviewRepository
from bee_slack_app.repository.user_repository import UserRepository
from bee_slack_app.utils import datetime

review_repository = ReviewRepository()
user_repository = UserRepository()


class GetConditions(TypedDict):
    score_for_me: Optional[str]
    score_for_others: Optional[str]


class ReviewItemKey(TypedDict):
    user_id: str
    isbn: str


class GetResponse(TypedDict):
    items: list[ReviewContents]
    keys: list[Union[ReviewItemKey, str]]


def get_review(*, logger: Any, user_id: str, isbn: str) -> Optional[ReviewContents]:
    """
    レビューを一意に指定して取得する
    """
    try:
        review = review_repository.get(user_id=user_id, isbn=isbn)

        if not review:
            return None

        user = user_repository.get(user_id)

        review["user_name"] = user["user_name"] if user else review["user_id"]

        return review

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def get_reviews(  # pylint: disable=dangerous-default-value
    *,
    logger: Any,
    conditions: Optional[GetConditions] = None,
    limit: Optional[int] = None,
    keys: list[ReviewItemKey] = [],
) -> Optional[GetResponse]:
    """
    次のlimit分のレビューを取得する

    Returns
        items: 取得したレビューのリスト
        keys: 更新された読み込みキーのリスト。これ以上アイテムが存在しない場合は、リストの最後の要素が"end"となる。
    """
    try:

        start_key = keys[-1] if len(keys) > 0 else None

        reviews = review_repository.get_some(
            conditions=conditions, limit=limit, start_key=start_key
        )

        fill_user_name(reviews["items"])

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

        reviews = review_repository.get_some(
            conditions=conditions, limit=limit, start_key=start_key
        )

        fill_user_name(reviews["items"])

        return {
            "items": reviews["items"],
            "keys": [reviews["last_key"]] if is_move_to_first else keys[:-1],  # type: ignore
        }

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def fill_user_name(review_contents_list: list[ReviewContents]) -> None:
    # 対応するユーザ情報からユーザ名を取得してレビュー情報に追加する
    users = user_repository.get_all()
    for review_contents in review_contents_list:
        user_candidate = [
            user for user in users if user["user_id"] == review_contents["user_id"]
        ]
        if len(user_candidate) == 1:
            user_name = user_candidate[0]["user_name"]
        else:
            # 対応するユーザ情報が存在しない場合はユーザIDを返す
            user_name = review_contents["user_id"]

        review_contents["user_name"] = user_name


def post_review(
    logger: Any, review_contents: ReviewContents
) -> Optional[ReviewContents]:
    try:
        item: ReviewContents = {
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
            "description": review_contents["description"],
        }
        review_repository.create(item)

        return item

    except Exception as error:  # pylint: disable=broad-except
        logger.exception(f"Failed to store data {error}")
        return None
