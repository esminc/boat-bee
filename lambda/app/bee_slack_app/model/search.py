from typing import Optional, TypedDict


class SearchedBook(TypedDict):
    title: str
    isbn: str
    authors: list[str]
    image_url: Optional[str]
    google_books_url: str
    description: str
