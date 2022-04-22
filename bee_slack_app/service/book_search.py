from typing import List, Optional

from bee_slack_app.model.search import SearchedBook
from bee_slack_app.repository.google_books_api import GoogleBooksApi

api_client = GoogleBooksApi()


def search_book_by_title(target_title: str) -> List[SearchedBook]:
    """
    タイトルから書籍を検索する

    Args:
        title : 検索したい書籍のタイトル（曖昧検索も可能）
    Returns:
        list: ヒットした書籍の辞書形式データをリストで格納する
    """

    books = api_client.search_book_by_title(target_title)

    results = []

    for book in books:
        book_info: SearchedBook = {
            "title": book["title"],
            "isbn": book["isbn"],
            "author": book["author"],
            "image_url": book["image_url"],
            "google_books_url": book["google_books_url"],
        }

        results.append(book_info)

    return results


def search_book_by_isbn(isbn: str) -> Optional[SearchedBook]:
    """
    ISBNから書籍を検索する

    Args:
        isbn : 検索したい書籍のISBN(13桁の数字、ハイフンなし)
    Returns:
        dict_info : ヒットした書籍の情報を辞書形式で返す
                    ヒットしなかった場合はNoneを返す
    """

    book = api_client.search_book_by_isbn(isbn)

    if book is None:
        return None

    book_info: SearchedBook = {
        "title": book["title"],
        "isbn": book["isbn"],
        "author": book["author"],
        "image_url": book["image_url"],
        "google_books_url": book["google_books_url"],
    }

    return book_info
