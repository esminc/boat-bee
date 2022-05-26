from typing import Any, TypedDict


class UserAction(TypedDict):
    """
    ユーザの行動履歴
    """

    user_id: str
    created_at: str
    action_type: str
    status: str
    payload: Any
