# pylint: disable=non-ascii-name


from logging import getLogger

from bee_slack_app.repository.book_review import BookReview
from bee_slack_app.repository.user_repository import UserRepository
from bee_slack_app.service.review import get_reviews


def test_レビューを取得できること(monkeypatch):
    def mock_book_review_repository_get(_, **__):
        return {
            "items": [
                {
                    "user_id": "user_id_0",
                    "user_name": "user_name_0",
                    "book_title": "仕事ではじめる機械学習",
                    "isbn": "12345",
                    "score_for_me": "1",
                    "score_for_others": "5",
                    "review_comment": "とても良いです",
                    "book_image_url": "dummy_book_image_url_0",
                    "book_author": "dummy_book_author_0",
                    "book_url": "dummy_book_url_0",
                },
                {
                    "user_id": "user_id_1",
                    "user_name": "user_name_1",
                    "book_title": "仕事ではじめる機械学習",
                    "isbn": "12345",
                    "score_for_me": "3",
                    "score_for_others": "4",
                    "review_comment": "まあまあです",
                    "book_image_url": "dummy_book_image_url_1",
                    "book_author": "dummy_book_author_1",
                    "book_url": "dummy_book_url_1",
                },
                {
                    "user_id": "user_id_2",
                    "user_name": "user_name_2",
                    "book_title": "Python チュートリアル",
                    "isbn": "67890",
                    "score_for_me": "2",
                    "score_for_others": "4",
                    "review_comment": "そこそこです",
                    "book_image_url": "dummy_book_image_url_2",
                    "book_author": "dummy_book_author_2",
                    "book_url": "dummy_book_url_2",
                },
            ],
            "last_key": None,
        }

    monkeypatch.setattr(BookReview, "get", mock_book_review_repository_get)

    reviews = get_reviews(logger=getLogger(), limit=10, keys=[])["items"]

    assert len(reviews) == 3

    assert reviews[0]["user_id"] == "user_id_0"
    assert reviews[0]["user_name"] == "user_name_0"
    assert reviews[0]["isbn"] == "12345"
    assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[0]["score_for_me"] == "1"
    assert reviews[0]["score_for_others"] == "5"
    assert reviews[0]["review_comment"] == "とても良いです"
    assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
    assert reviews[0]["book_author"] == "dummy_book_author_0"
    assert reviews[0]["book_url"] == "dummy_book_url_0"

    assert reviews[1]["user_id"] == "user_id_1"
    assert reviews[1]["user_name"] == "user_name_1"
    assert reviews[1]["isbn"] == "12345"
    assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[1]["score_for_me"] == "3"
    assert reviews[1]["score_for_others"] == "4"
    assert reviews[1]["review_comment"] == "まあまあです"
    assert reviews[1]["book_image_url"] == "dummy_book_image_url_1"
    assert reviews[1]["book_author"] == "dummy_book_author_1"
    assert reviews[1]["book_url"] == "dummy_book_url_1"

    assert reviews[2]["user_id"] == "user_id_2"
    assert reviews[2]["user_name"] == "user_name_2"
    assert reviews[2]["isbn"] == "67890"
    assert reviews[2]["book_title"] == "Python チュートリアル"
    assert reviews[2]["score_for_me"] == "2"
    assert reviews[2]["score_for_others"] == "4"
    assert reviews[2]["review_comment"] == "そこそこです"
    assert reviews[2]["book_image_url"] == "dummy_book_image_url_2"
    assert reviews[2]["book_author"] == "dummy_book_author_2"
    assert reviews[2]["book_url"] == "dummy_book_url_2"


def test_book_review_repositoryの処理でエラーが発生した場合Noneを返すこと(
    monkeypatch,
):  # pylint: disable=invalid-name
    def mock_book_review_repository_get(_, __):
        raise Exception("dummy exception")

    monkeypatch.setattr(UserRepository, "get_all", mock_book_review_repository_get)

    reviews = get_reviews(logger=getLogger(), limit=10, keys=[])

    assert reviews is None


def test_user_repositoryの処理でエラーが発生した場合Noneを返すこと(
    monkeypatch,
):  # pylint: disable=invalid-name
    def mock_user_repository_get_all(_, __):
        raise Exception("dummy exception")

    monkeypatch.setattr(BookReview, "get", mock_user_repository_get_all)

    reviews = get_reviews(logger=getLogger(), limit=10, keys=[])

    assert reviews is None
