from typing import Optional, TypedDict


class User(TypedDict):
    user_id: str
    user_name: str
    department: str
    job_type: str
    age_range: str
    updated_at: Optional[str]
