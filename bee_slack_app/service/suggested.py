from logging import getLogger
from typing import Optional

from bee_slack_app.model.suggested_book import SuggestedBook
from bee_slack_app.repository import SuggestedBookRepository
from bee_slack_app.utils import datetime

suggested_book_repository = SuggestedBookRepository()


def create_initial_suggested(*, user_id: str, isbn: str, ml_model: str) -> None:
    """
    おすすめ本が未登録の場合はそれを登録する

    Args:
        user_id : おすすめされたユーザーのuser_id
        isbn    : おすすめされた本のisbn
        ml_model: おすすめされた本のml_model

    Returns:
        なし
    """
    logger = getLogger(__name__)
    try:
        result = suggested_book_repository.get(
            user_id=user_id, isbn=isbn, ml_model=ml_model
        )
        if result is None:
            suggested_book_repository.create(
                {
                    "user_id": user_id,
                    "isbn": isbn,
                    "ml_model": ml_model,
                    "interested": False,
                    "updated_at": datetime.now(),
                }
            )
    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")


def get_is_interested(*, user_id: str, isbn: str, ml_model: str) -> Optional[bool]:
    """
    おすすめされた本の情報（履歴）を取得する

    Args:
        user_id : おすすめされたユーザーのuser_id
        isbn    : おすすめされた本のisbn
        ml_model: おすすめされた本のml_model


    Returns:
        興味あり:True、興味なし:False、未登録の場合は、Falseを返す。
    """
    logger = getLogger(__name__)

    try:
        result: Optional[SuggestedBook] = suggested_book_repository.get(
            user_id=user_id, isbn=isbn, ml_model=ml_model
        )
        return False if result is None else result["interested"]

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def add_suggested(suggested_book: SuggestedBook) -> None:
    """
    おすすめされた本の情報（履歴）を登録・更新する
    """
    logger = getLogger(__name__)

    try:
        suggested_book_repository.create(
            {
                "user_id": suggested_book["user_id"],
                "isbn": suggested_book["isbn"],
                "ml_model": suggested_book["ml_model"],
                "interested": suggested_book["interested"],
                "updated_at": datetime.now(),
            }
        )

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to store data")
