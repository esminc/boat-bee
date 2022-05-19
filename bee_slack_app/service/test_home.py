# pylint: disable=non-ascii-name

from logging import getLogger

from bee_slack_app.repository.review_repository import ReviewRepository
from bee_slack_app.service.home import home


def test_レビュー投稿数を取得できること(monkeypatch):

    items = [
        {
            "user_id": "user_id_0",
            "isbn": "12345",
            "book_title": "仕事ではじめる機械学習",
            "score_for_me": "3",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        },
        {
            "user_id": "user_id_1",
            "isbn": "12345",
            "book_title": "仕事で使える機械学習",
            "score_for_me": "4",
            "score_for_others": "3",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
        },
    ]

    def mock_get_some():
        return items

    monkeypatch.setattr(ReviewRepository, "get_some", mock_get_some)

    logger = getLogger()
    review_count_all = home(logger)

    assert review_count_all == 2
