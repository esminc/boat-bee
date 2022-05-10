# pylint: disable=duplicate-code
# pylint: disable=non-ascii-name


from logging import getLogger

from bee_slack_app.repository.book_review import BookReview
from bee_slack_app.repository.google_books import GoogleBooks
from bee_slack_app.service.review import get_reviews, post_review
from bee_slack_app.utils import datetime


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
            },
            {
                "user_id": "user_id_1",
                "book_title": "仕事ではじめる機械学習",
                "isbn": "12345",
                "score_for_me": "3",
                "score_for_others": "4",
                "review_comment": "まあまあです",
            },
            {
                "user_id": "user_id_2",
                "book_title": "Python チュートリアル",
                "isbn": "67890",
                "score_for_me": "2",
                "score_for_others": "4",
                "review_comment": "そこそこです",
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

    assert reviews[1]["user_id"] == "user_id_1"
    assert reviews[1]["isbn"] == "12345"
    assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[1]["score_for_me"] == "3"
    assert reviews[1]["score_for_others"] == "4"
    assert reviews[1]["review_comment"] == "まあまあです"

    assert reviews[2]["user_id"] == "user_id_2"
    assert reviews[2]["isbn"] == "67890"
    assert reviews[2]["book_title"] == "Python チュートリアル"
    assert reviews[2]["score_for_me"] == "2"
    assert reviews[2]["score_for_others"] == "4"
    assert reviews[2]["review_comment"] == "そこそこです"


def test_repositoryの処理でエラーが発生した場合Noneを返すこと(monkeypatch):  # pylint: disable=invalid-name
    def mock_book_review_repository_get(_, __):
        raise Exception("dummy exception")

    monkeypatch.setattr(BookReview, "get", mock_book_review_repository_get)

    reviews = get_reviews(getLogger())

    assert reviews is None


def test_レビューを投稿できること(mocker):  # pylint: disable=invalid-name
    mocker.patch.object(datetime, "now").return_value = "2022-04-01T00:00:00+09:00"

    mock_google_books_repository_search_book_by_isbn = mocker.patch.object(
        GoogleBooks, "search_book_by_isbn"
    )
    mock_google_books_repository_search_book_by_isbn.return_value = {
        "image_url": "dummy_url"
    }

    mock_book_review_repository_create = mocker.patch.object(BookReview, "create")

    review = {
        "user_id": "user_id_0",
        "book_title": "仕事ではじめる機械学習",
        "isbn": "12345",
        "score_for_me": "5",
        "score_for_others": "5",
        "review_comment": "とても良いです",
    }

    post_review(getLogger(), review)

    assert mock_google_books_repository_search_book_by_isbn.call_count == 1
    assert mock_google_books_repository_search_book_by_isbn.call_args.args[0] == "12345"
    assert mock_book_review_repository_create.call_count == 1
    assert mock_book_review_repository_create.call_args.args[0] == {
        "user_id": "user_id_0",
        "book_title": "仕事ではじめる機械学習",
        "isbn": "12345",
        "score_for_me": "5",
        "score_for_others": "5",
        "review_comment": "とても良いです",
        "updated_at": "2022-04-01T00:00:00+09:00",
        "image_url": "dummy_url",
    }


def test_image_url無しでレビューを投稿できること(mocker):  # pylint: disable=invalid-name
    mocker.patch.object(datetime, "now").return_value = "2022-04-01T00:00:00+09:00"

    mock_google_books_repository_search_book_by_isbn = mocker.patch.object(
        GoogleBooks, "search_book_by_isbn"
    )
    mock_google_books_repository_search_book_by_isbn.return_value = None

    mock_book_review_repository_create = mocker.patch.object(BookReview, "create")

    review = {
        "user_id": "user_id_0",
        "book_title": "仕事ではじめる機械学習",
        "isbn": "12345",
        "score_for_me": "5",
        "score_for_others": "5",
        "review_comment": "とても良いです",
    }

    post_review(getLogger(), review)

    assert mock_google_books_repository_search_book_by_isbn.call_count == 1
    assert mock_google_books_repository_search_book_by_isbn.call_args.args[0] == "12345"
    assert mock_book_review_repository_create.call_count == 1
    assert mock_book_review_repository_create.call_args.args[0] == {
        "user_id": "user_id_0",
        "book_title": "仕事ではじめる機械学習",
        "isbn": "12345",
        "score_for_me": "5",
        "score_for_others": "5",
        "review_comment": "とても良いです",
        "updated_at": "2022-04-01T00:00:00+09:00",
        "image_url": None,
    }
