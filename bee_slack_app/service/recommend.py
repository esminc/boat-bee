from typing import Any, Optional

from bee_slack_app.model.search import SearchedBook
from bee_slack_app.model.user import User
from bee_slack_app.repository.google_books_repository import GoogleBooksRepository
from bee_slack_app.repository.recommend_book_repository import RecommendBookRepository

recommend_book_repository = RecommendBookRepository()


def recommend(logger: Any, user: User) -> Optional[SearchedBook]:
    """
    おすすめの本の情報を返却する

    Args:
        user : おすすめ本を知りたい、利用者のユーザ情報。

    Returns:
        book: おすすめする本の情報。取得できない場合は、Noneが返る。
    """
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

        isbn = recommend_book_repository.fetch(user_id)

        if not isbn:
            logger.info("Failed to recommend book. user_id: ", user_id)
            return None

        book_info = GoogleBooksRepository().search_book_by_isbn(isbn)
        book: Optional[SearchedBook] = None
        results = []
        if book_info is not None:
            for book in book_info:
                book = {
                    "title": book_info["title"],
                    "isbn": isbn,
                    "authors": book_info["authors"],
                    "google_books_url": book_info["google_books_url"],
                    "image_url": book_info["image_url"],
                    "description": book_info["description"],
                }
                results.append(book)
        return results

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None
