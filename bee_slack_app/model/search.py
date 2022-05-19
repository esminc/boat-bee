from typing import Optional, TypedDict


class SearchedBook(TypedDict):
    title: str
    isbn: str
    authors: str
    image_url: Optional[str]
    google_books_url: str
