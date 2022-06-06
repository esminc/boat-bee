from logging import getLogger
from typing import Optional

from bee_slack_app.model.suggested_book import SuggestedBook
from bee_slack_app.repository.suggested_book_repository import SuggestedBookRepository
from bee_slack_app.utils import datetime

suggested_book_repository = SuggestedBookRepository()


def get_suggested(*, user_id: str, isbn: str, ml_model: str) -> Optional[SuggestedBook]:
    """
    おすすめされた本の情報（履歴）を取得する

    Args:
        user_id : おすすめされたユーザーのuser_id
        isbn    : おすすめされた本のisbn
        ml_model: おすすめされた本のml_model


    Returns:
        SuggestedBook: おすすめされた本の情報（履歴）。未登録の場合は、Noneが返る。
    """
    logger = getLogger(__name__)

    try:
        return suggested_book_repository.get(
            user_id=user_id, isbn=isbn, ml_model=ml_model
        )

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