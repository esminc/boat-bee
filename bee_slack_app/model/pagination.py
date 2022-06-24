from typing import TypedDict

from bee_slack_app.model.review import ReviewContents


class ReviewPagination(TypedDict):
    reviews: list[ReviewContents]
    show_move_to_back: bool
    show_move_to_next: bool
