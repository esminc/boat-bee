from logging import getLogger
from typing import Any, Optional, TypedDict

from bee_slack_app.model import Book
from bee_slack_app.repository import BookRepository

book_repository = BookRepository()


class GetBooksResponse(TypedDict):
    items: list[Book]
    keys: Any
    has_next: bool


def get_books(
    *,
    limit: Optional[int] = None,
    keys: Any = None,
) -> Optional[GetBooksResponse]:
    """
    レビューが投稿されている本のリストを取得する

    Args:
        limit: 一度に取得する本の数
        keys: 読み込みキーのリスト

    Returns
        items: 取得した本のリスト
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

        books = book_repository.fetch_all(limit=limit, start_key=start_key)

        logger.info(books)

        last_key = [books["last_key"]] if books["last_key"] else ["end"]  # type: ignore
        has_next = last_key != ["end"]

        return {"items": books["items"], "keys": keys + last_key, "has_next": has_next}

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


class GetBooksBeforeResponse(TypedDict):
    items: list[Book]
    keys: Any
    is_move_to_first: bool


def get_books_before(
    *,
    limit: int,
    keys: Any = None,
) -> Optional[GetBooksBeforeResponse]:
    """
    レビューが投稿されている本のリストを取得する（前への移動）

    keysの状態より1ページ前の本のリストを取得する。
    例えば、keysが3ページ目を指しているならば、2ページ目の本のリストを取得する。

    Returns
        items: 取得した本のリスト
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

        books = book_repository.fetch_all(limit=limit, start_key=start_key)

        logger.info(books)

        return {
            "items": books["items"],
            "keys": [books["last_key"]] if is_move_to_first else keys[:-1],
            "is_move_to_first": is_move_to_first,
        }

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def _is_valid_key(target) -> bool:
    return isinstance(target, list)
