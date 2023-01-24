from logging import getLogger
from typing import Optional, TypedDict

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


RecommendResult = TypedDict(
    "RecommendResult", {"recommended_books": list[RecommendBook], "created_at": str}
)


def recommend(user: User) -> Optional[RecommendResult]:
    """
    おすすめの本の情報を返却する

    Args:
        user : おすすめ本を知りたい、利用者のユーザ情報。

    Returns:
        おすすめの本の情報
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

        recommend_book_fetch_result = recommend_book_repository.fetch(user_id)

        if not recommend_book_fetch_result:
            logger.info("Failed to recommend book")
            logger.info({"user_id": user_id})
            return None

        recommended_books = []
        for book_recommendation in recommend_book_fetch_result["book_recommendations"]:
            isbn = book_recommendation["isbn"]
            ml_model = book_recommendation["ml_model_name"]

            book = book_repository.fetch(isbn=isbn)
            if book is not None:
                suggested_book = suggested_book_repository.fetch(
                    user_id=user["user_id"], isbn=isbn, ml_model=ml_model
                )

                if not suggested_book:
                    # おすすめ本が未登録の場合はそれを登録する
                    suggested_book_repository.put(
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

        return {
            "recommended_books": recommended_books,
            "created_at": recommend_book_fetch_result["created_at"],
        }

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None


def update_suggested_book_state(suggested_book: SuggestedBook) -> None:
    """
    おすすめされた本の情報（履歴）を登録・更新する
    """
    logger = getLogger(__name__)

    try:
        suggested_book_repository.put(
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
