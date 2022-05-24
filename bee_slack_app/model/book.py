from typing import TypedDict


class Book(TypedDict):
    """
    本
    """

    isbn: str
    title: str
    author: str
    url: str
    image_url: str
    updated_at: str
