# pylint: disable=duplicate-code
# pylint: disable=non-ascii-name


from logging import getLogger

from bee_slack_app.repository.book_review import BookReview
from bee_slack_app.service.review import get_reviews


def test_レビューを取得できること(monkeypatch):
    def mock_book_review_repository_get(_, __):
        return [
            {
                "user_id": "user_id_0",
                "book_title": "仕事ではじめる機械学習",
                "isbn": "12345",
                "score_for_me": "1",
                "score_for_others": "5",
                "review_comment": "とても良いです",
                "image_url": "dummy_image_url_0",
                "author": "dummy_author_0",
                "url": "dummy_url_0",
            },
            {
                "user_id": "user_id_1",
                "book_title": "仕事ではじめる機械学習",
                "isbn": "12345",
                "score_for_me": "3",
                "score_for_others": "4",
                "review_comment": "まあまあです",
                "image_url": "dummy_image_url_1",
                "author": "dummy_author_1",
                "url": "dummy_url_1",
            },
            {
                "user_id": "user_id_2",
                "book_title": "Python チュートリアル",
                "isbn": "67890",
                "score_for_me": "2",
                "score_for_others": "4",
                "review_comment": "そこそこです",
                "image_url": "dummy_image_url_2",
                "author": "dummy_author_2",
                "url": "dummy_url_2",
            },
        ]

    monkeypatch.setattr(BookReview, "get", mock_book_review_repository_get)

    reviews = get_reviews(getLogger())

    assert len(reviews) == 3

    assert reviews[0]["user_id"] == "user_id_0"
    assert reviews[0]["isbn"] == "12345"
    assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[0]["score_for_me"] == "1"
    assert reviews[0]["score_for_others"] == "5"
    assert reviews[0]["review_comment"] == "とても良いです"
    assert reviews[0]["image_url"] == "dummy_image_url_0"
    assert reviews[0]["author"] == "dummy_author_0"
    assert reviews[0]["url"] == "dummy_url_0"

    assert reviews[1]["user_id"] == "user_id_1"
    assert reviews[1]["isbn"] == "12345"
    assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[1]["score_for_me"] == "3"
    assert reviews[1]["score_for_others"] == "4"
    assert reviews[1]["review_comment"] == "まあまあです"
    assert reviews[1]["image_url"] == "dummy_image_url_1"
    assert reviews[1]["author"] == "dummy_author_1"
    assert reviews[1]["url"] == "dummy_url_1"

    assert reviews[2]["user_id"] == "user_id_2"
    assert reviews[2]["isbn"] == "67890"
    assert reviews[2]["book_title"] == "Python チュートリアル"
    assert reviews[2]["score_for_me"] == "2"
    assert reviews[2]["score_for_others"] == "4"
    assert reviews[2]["review_comment"] == "そこそこです"
    assert reviews[2]["image_url"] == "dummy_image_url_2"
    assert reviews[2]["author"] == "dummy_author_2"
    assert reviews[2]["url"] == "dummy_url_2"


def test_repositoryの処理でエラーが発生した場合Noneを返すこと(monkeypatch):  # pylint: disable=invalid-name
    def mock_book_review_repository_get(_, __):
        raise Exception("dummy exception")

    monkeypatch.setattr(BookReview, "get", mock_book_review_repository_get)

    reviews = get_reviews(getLogger())

    assert reviews is None
