from typing import Any, Optional

from bee_slack_app.model.search import SearchedBook
from bee_slack_app.model.user import User
from bee_slack_app.repository.google_books import GoogleBooks


def recommend(logger: Any, user: User) -> Optional[SearchedBook]:
    """
    おすすめのブック情報を返却する

    Args:
        user : おすすめ本を知りたい、利用者のユーザ情報。

    Returns:
        book: おすすめするブック情報。取得できない場合は、Noneが返る。
    """
    # TODO 機械学習の部品が実装できたら、部品を呼び出す。
    # TODO 取得したisbnからブック情報を取得する。
    print(user)
    isbn = "9784873118253"

    try:
        google_books = GoogleBooks()
        book_info = google_books.search_book_by_isbn(isbn)
        print(book_info)
        return book_info

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return None
