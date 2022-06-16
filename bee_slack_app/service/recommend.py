from logging import getLogger
from typing import Optional

from bee_slack_app.model import RecommendBook, SuggestedBook, User
from bee_slack_app.repository import (
    BookRepository,
    RecommendBookRepository,
    SuggestedBookRepository,
)
from bee_slack_app.utils import datetime

book_repository = BookRepository()
recommend_book_repository = RecommendBookRepository()
suggested_book_repository = SuggestedBookRepository()


def recommend(user: User) -> list[RecommendBook]:
    """
    おすすめの本の情報を返却する

    Args:
        user : おすすめ本を知りたい、利用者のユーザ情報。

    Returns:
        おすすめする本のリスト
    """
    logger = getLogger(__name__)

    try:
        # デバッグ用
        # FDOワークスペース及びBEE_TESTのユーザIDの場合、対応するITSワークスペースのユーザIDに変換する
        user_id = user["user_id"]
        user_id_in_fdo_workspace = {
            "U029SGVM1AA": "U02K1KEB4U9",
            "U029JHRHC15": "U02JP1YKX4K",
            "U029Z9HAK6E": "U034EPH70TB",
            "U02A5F5KXKN": "U032CTY4KD3",
            "U01DT6X2MH8": "U02UU55VDRU",
            "U03BD92HA76": "U02K1KEB4U9",  # BEE_TEST 坂部
            "U03BAUEM5QS": "U02JP1YKX4K",  # BEE_TEST 岡本
            "U03B49AKZV4": "U034EPH70TB",  # BEE_TEST 三田村
            "U03B822P6S1": "U032CTY4KD3",  # BEE_TEST 見澤
        }
        user_id = user_id_in_fdo_workspace.get(user_id, user_id)

        recommended_book_dict = recommend_book_repository.fetch(user_id)

        if not recommended_book_dict:
            logger.info("Failed to recommend book")
            logger.info({"user_id": user_id})
            return []

        recommended_books = []
        for ml_model, isbn in recommended_book_dict.items():
            book = book_repository.fetch(isbn=isbn)
            if book is not None:
                suggested_book = suggested_book_repository.get(
                    user_id=user["user_id"], isbn=isbn, ml_model=ml_model
                )

                if not suggested_book:
                    # おすすめ本が未登録の場合はそれを登録する
                    suggested_book_repository.create(
                        {
                            "user_id": user["user_id"],
                            "isbn": isbn,
                            "ml_model": ml_model,
                            "interested": False,
                            "updated_at": datetime.now(),
                        }
                    )

                interested = suggested_book["interested"] if suggested_book else False

                recommended_book: RecommendBook = {
                    "title": book["title"],
                    "isbn": isbn,
                    "author": book["author"],
                    "url": book["url"],
                    "image_url": book["image_url"],
                    "description": book["description"],
                    "updated_at": book["updated_at"],
                    "interested": interested,
                    "ml_model": ml_model,
                }
                recommended_books.append(recommended_book)

        return recommended_books

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return []


def created_at() -> Optional[str]:
    """
    おすすめ情報の生成時刻をISO 8601形式で取得する
    ISO 8601形式であることは情報を格納するbee-ml側で担保すること

    Returns:
        str : YYYY/mm/dd HH:MM:SSの時刻文字列。例 2022/04/01 00:00:00
    """
    logger = getLogger(__name__)

    try:
        metadata = RecommendBookRepository().fetch_metadata()

        return metadata.get("created_at") if metadata is not None else None

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def update_suggested_book_state(suggested_book: SuggestedBook) -> None:
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
