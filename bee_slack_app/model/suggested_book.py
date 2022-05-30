from typing import TypedDict


class SuggestedBook(TypedDict):
    user_id: str
    isbn: str
    ml_model: str
    interested: bool
    updated_at: str
