from logging import getLogger
from typing import Optional

from bee_slack_app.model.search import SearchedBook
from bee_slack_app.model.user import User
from bee_slack_app.repository.google_books_repository import GoogleBooksRepository
from bee_slack_app.repository.recommend_book_repository import RecommendBookRepository

recommend_book_repository = RecommendBookRepository()


def recommend(user: User) -> list[tuple[SearchedBook, str]]:
    """
    おすすめの本の情報を返却する

    Args:
        user : おすすめ本を知りたい、利用者のユーザ情報。

    Returns:
        book: おすすめする本の情報。
        ml_model:おすすめした機械学習のモデル
    """
    logger = getLogger(__name__)

    try:
        # デバッグ用
        # FDOワークスペースのユーザIDの場合、対応するITSワークスペースのユーザIDに変換する
        user_id = user["user_id"]
        user_id_in_fdo_workspace = {
            "U029SGVM1AA": "U02K1KEB4U9",
            "U029JHRHC15": "U02JP1YKX4K",
            "U029Z9HAK6E": "U034EPH70TB",
            "U02A5F5KXKN": "U032CTY4KD3",
            "U01DT6X2MH8": "U02UU55VDRU",
        }
        user_id = user_id_in_fdo_workspace.get(user_id, user_id)

        recommended_book_dict = recommend_book_repository.fetch(user_id)

        if not recommended_book_dict:
            logger.info("Failed to recommend book")
            logger.info({"user_id": user_id})
            return []

        recommended_books = []
        for ml_model, isbn in recommended_book_dict.items():
            book = GoogleBooksRepository().search_book_by_isbn(isbn)
            if book is not None:
                book_info: SearchedBook = {
                    "title": book["title"],
                    "isbn": isbn,
                    "authors": book["authors"],
                    "google_books_url": book["google_books_url"],
                    "image_url": book["image_url"],
                    "description": book["description"],
                }
                item = (book_info, ml_model)
                recommended_books.append(item)
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
