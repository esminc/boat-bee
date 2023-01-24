from logging import getLogger
from typing import Any, Optional, TypedDict

from bee_slack_app.model import Book, Review
from bee_slack_app.repository import BookRepository, ReviewRepository, UserRepository
from bee_slack_app.utils import datetime

review_repository = ReviewRepository()
user_repository = UserRepository()
book_repository = BookRepository()


def get_review(*, user_id: str, isbn: str) -> Optional[Review]:
    """
    レビューを一意に指定して取得する
    """
    logger = getLogger(__name__)

    try:
        review = review_repository.fetch(user_id=user_id, isbn=isbn)

        if not review:
            return None

        user = user_repository.fetch(user_id)

        review["user_name"] = user["user_name"] if user else review["user_id"]

        return review

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def get_review_all() -> Optional[list[Review]]:
    """
    全てのレビューを取得する

    Returns: 取得したレビューのリスト
    """
    logger = getLogger(__name__)

    try:

        reviews = review_repository.fetch_all()

        fill_user_name(reviews)

        return reviews

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def get_reviews_by_isbn(*, isbn: str) -> Optional[list[Review]]:
    """
    ISBNからレビューを取得する
    """
    try:
        logger = getLogger(__name__)

        reviews = review_repository.fetch_by_isbn(isbn=isbn)

        fill_user_name(reviews)

        logger.info({"reviews": reviews})

        return reviews

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def get_reviews_by_user_id(*, user_id: str) -> Optional[list[Review]]:
    """
    ユーザIDからレビューを取得する
    """
    try:
        logger = getLogger(__name__)

        reviews = review_repository.fetch_by_user_id(user_id=user_id)

        fill_user_name(reviews)

        logger.info({"reviews": reviews})

        return reviews

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def fill_user_name(review_contents_list: list[Review]) -> None:
    # 対応するユーザ情報からユーザ名を取得してレビュー情報に追加する
    users = user_repository.fetch_all()
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


def post_review(review_contents: Review) -> Optional[Review]:

    logger = getLogger(__name__)

    try:
        updated_at = datetime.now()

        item: Review = {
            "user_id": review_contents["user_id"],
            "book_title": review_contents["book_title"],
            "isbn": review_contents["isbn"],
            "score_for_me": review_contents["score_for_me"],
            "score_for_others": review_contents["score_for_others"],
            "review_comment": review_contents["review_comment"],
            "updated_at": updated_at,
            "book_image_url": review_contents["book_image_url"],
            "book_author": review_contents["book_author"],
            "book_url": review_contents["book_url"],
            "book_description": review_contents["book_description"],
        }
        review_repository.put(item)

        book: Book = {
            "isbn": review_contents["isbn"],
            "title": review_contents["book_title"],
            "author": review_contents["book_author"],
            "url": review_contents["book_url"],
            "image_url": review_contents["book_image_url"],
            "description": review_contents["book_description"],
            "updated_at": updated_at,
        }

        book_repository.put(book=book)

        post_review_count = len(
            review_repository.fetch_by_user_id(user_id=review_contents["user_id"])
        )

        user_repository.update_post_review_count(
            user_id=review_contents["user_id"], count=post_review_count
        )

        return item

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to store data")
        return None


class GetNextReviewsResponse(TypedDict):
    items: list[Review]
    keys: Any
    has_next: bool


def get_next_reviews_by_user_id(
    *,
    user_id: str,
    limit: int,
    keys: Any = None,
) -> Optional[GetNextReviewsResponse]:
    """
    ユーザIDからレビューを順方向に取得する

    Args:
        user_id: レビューを取得したいユーザー
        limit: 一度に取得するレビューの数
        keys: 読み込みキーのリスト

    Returns
        items: 取得したレビューのリスト
        keys: 更新された読み込みキーのリスト
        has_next: さらに読み込む要素があるか
    """
    try:
        logger = getLogger(__name__)

        if not keys:
            keys = []

        if not _is_valid_key(keys):
            logger.info({"keys": keys})
            return None

        start_key = keys[-1] if len(keys) > 0 else None

        reviews = review_repository.fetch_limited_by_user_id(
            user_id=user_id, limit=limit, start_key=start_key
        )

        fill_user_name(reviews["items"])

        logger.info({"reviews": reviews})

        last_key = [reviews["last_key"]] if reviews["last_key"] else ["end"]  # type: ignore
        has_next = last_key != ["end"]

        return {
            "items": reviews["items"],
            "keys": keys + last_key,
            "has_next": has_next,
        }

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get next data.")
        return None


class GetBeforeReviewsResponse(TypedDict):
    items: list[Review]
    keys: Any
    is_move_to_first: bool


def get_before_reviews_by_user_id(
    *,
    user_id: str,
    limit: int,
    keys: Any = None,
) -> Optional[GetBeforeReviewsResponse]:
    """
    ユーザIDからレビューを逆方向に取得する

    keysの状態より1ページ前のレビューリストを取得する。
    例えば、keysが3ページ目を指しているならば、2ページ目のレビューリストを取得する。

    Args:
        user_id: レビューを取得したいユーザー
        limit: 一度に取得するレビューの数
        keys: 読み込みキーのリスト

    Returns
        items: 取得したレビューのリスト
        keys: 更新された読み込みキーのリスト
        is_move_to_first: 0ページへの遷移か
    """
    try:
        logger = getLogger(__name__)

        if not keys:
            keys = []

        if not _is_valid_key(keys):
            logger.info({"keys": keys})
            return None

        is_move_to_first = len(keys) < 3

        start_key = None if is_move_to_first else keys[-3]

        reviews = review_repository.fetch_limited_by_user_id(
            user_id=user_id, limit=limit, start_key=start_key
        )

        fill_user_name(reviews["items"])

        logger.info({"reviews": reviews})

        return {
            "items": reviews["items"],
            "keys": [reviews["last_key"]] if is_move_to_first else keys[:-1],
            "is_move_to_first": is_move_to_first,
        }

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get before data.")
        return None


def _is_valid_key(target) -> bool:
    return isinstance(target, list)
