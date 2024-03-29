from typing import Optional

from bee_slack_app.model import SearchedBook
from bee_slack_app.repository import GoogleBooksRepository

api_client = GoogleBooksRepository()


def search_book_by_title(title: str) -> list[SearchedBook]:
    """
    タイトルから書籍を検索する

    Args:
        title : 検索したい書籍のタイトル（曖昧検索も可能）
    Returns:
        list[SearchedBook] : ヒットした書籍の情報をSearchedBokのリスト形式で返す
                             ヒットしなかった場合は空のリストを返す
    """

    books = api_client.search_book_by_title(title)

    results = []

    for book in books:
        book_info: SearchedBook = {
            "title": book["title"],
            "isbn": book["isbn"],
            "authors": book["authors"],
            "image_url": book["image_url"],
            "google_books_url": book["google_books_url"],
            "description": book["description"],
        }

        results.append(book_info)

    return results


def search_book_by_isbn(isbn: str) -> Optional[SearchedBook]:
    """
    ISBNから書籍を検索する

    Args:
        isbn : 検索したい書籍のISBN(13桁の数字、ハイフンなし)
    Returns:
        Optional[SearchedBook] : ヒットした書籍の情報を返す
                                 ヒットしなかった場合はNoneを返す
    """

    book = api_client.search_book_by_isbn(isbn)

    if book is None:
        return None

    book_info: SearchedBook = {
        "title": book["title"],
        "isbn": book["isbn"],
        "authors": book["authors"],
        "image_url": book["image_url"],
        "google_books_url": book["google_books_url"],
        "description": book["description"],
    }

    return book_info
