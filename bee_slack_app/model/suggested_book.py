from typing import Optional, TypedDict


class SuggestedBook(TypedDict):
    user_id: str
    isbn: str
    ml_model: str
    interested: bool
    updated_at: Optional[str]
