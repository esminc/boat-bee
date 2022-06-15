from typing import Optional, TypedDict


class UserRequired(TypedDict):
    """
    Required keys
    """

    user_id: str
    user_name: str
    department: str
    job_type: str
    age_range: str
    updated_at: Optional[str]
    post_review_count: int


class User(UserRequired, total=False):
    """
    Optional keys
    """

    review_count: int
