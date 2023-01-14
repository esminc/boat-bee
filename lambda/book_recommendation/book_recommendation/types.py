from typing import Optional, TypedDict


class Review(TypedDict):
    user_id: str
    book_title: str
    isbn: str
    score_for_me: str
    score_for_others: str
    review_comment: str
    updated_at: Optional[str]
    book_image_url: str
    book_author: str
    book_url: str
    book_description: str


class SuggestedBook(TypedDict):
    user_id: str
    isbn: str
    ml_model: str
    interested: bool
    updated_at: Optional[str]
