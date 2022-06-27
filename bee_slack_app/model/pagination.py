from typing import TypedDict

from bee_slack_app.model.review import Review


class ReviewPagination(TypedDict):
    reviews: list[Review]
    show_move_to_back: bool
    show_move_to_next: bool
