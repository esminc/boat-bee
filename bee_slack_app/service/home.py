from typing import Any

from bee_slack_app.repository.review_repository import ReviewRepository


def home(logger: Any) -> int:
    """
    ホーム画面に表示するレビュー投稿数を返却する

    Args:
        なし

    Returns:
        review_count_all: レビュー投稿数。取得できない場合は、0が返る。
    """
    print("home_start")
    try:
        items = ReviewRepository().get_some()
        print(items)
        review_count_all = 0
        if items is not None:
            review_count_all = len(items)
        return review_count_all

    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to get data.")
        return 0
