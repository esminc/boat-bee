from typing import Optional, TypedDict


class ReviewContentsRequired(TypedDict):
    """
    Required keys
    """

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


class ReviewContents(ReviewContentsRequired, total=False):
    """
    Optional keys
    """

    user_name: str
