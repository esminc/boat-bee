from typing import TypedDict


class ReviewContents(TypedDict):
    user_id: str
    book_title: str
    isbn: str
    score_for_me: int
    score_for_others: int
    review_comment: str
