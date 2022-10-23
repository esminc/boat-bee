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
    description: str
    updated_at: str


class RecommendBook(Book):
    """
    おすすめの本
    """

    interested: bool
    ml_model: str
