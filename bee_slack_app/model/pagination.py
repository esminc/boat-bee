from typing import TypedDict


class ReviewPagination(TypedDict):
    reviews: list
    show_move_to_back: bool
    show_move_to_next: bool
