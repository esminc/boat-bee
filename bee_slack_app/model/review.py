from typing import TypedDict


class ReviewContents(TypedDict):
    user_id: str
    book_title: str
    isbn: str
    score_for_me: str
    score_for_others: str
    review_comment: str
    image_url: str
