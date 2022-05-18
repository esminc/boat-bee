# pylint: disable=non-ascii-name

from logging import getLogger

from bee_slack_app.model.user import User
from bee_slack_app.repository.google_books_repository import GoogleBooksRepository
from bee_slack_app.service.recommend import recommend


def test_おすすめの本の情報を取得できること(monkeypatch):
    def mock_search_book_by_isbn(_, isbn):
        return {
            "title": "仕事ではじめる機械学習",
            "isbn": isbn,
            "author": ["有賀康顕", "中山心太", "西林孝"],
            "google_books_url": "test_google_books_url",
            "image_url": "test_image_url",
        }

    monkeypatch.setattr(
        GoogleBooksRepository, "search_book_by_isbn", mock_search_book_by_isbn
    )

    user: User = {
        "user_id": "U03B49AKZV4",
        "user_name": "永和太郎",
        "department": "finance",
        "job_type": "engineer",
        "age_range": "60",
        "updated_at": None,
    }

    logger = getLogger()
    book = recommend(logger, user)

    assert book["title"] == "仕事ではじめる機械学習"
    assert book["isbn"] == "9784873118253"
    assert book["author"] == ["有賀康顕", "中山心太", "西林孝"]
    assert book["image_url"] == "test_image_url"
    assert book["google_books_url"] == "test_google_books_url"


def test_おすすめの本の情報がNoneのケース(monkeypatch):  # pylint: disable=invalid-name
    def mock_search_book_by_isbn(_, __):
        return None

    monkeypatch.setattr(
        GoogleBooksRepository, "search_book_by_isbn", mock_search_book_by_isbn
    )

    user: User = {
        "user_id": "U03B49AKZV4",
        "user_name": "永和太郎",
        "department": "finance",
        "job_type": "engineer",
        "age_range": "60",
        "updated_at": None,
    }

    logger = getLogger()
    book = recommend(logger, user)

    assert book is None


def test_おすすめ本の書影がNoneならNoneが返値に設定されること(monkeypatch):  # pylint: disable=invalid-name
    def mock_search_book_by_isbn(_, isbn):
        return {
            "title": "仕事ではじめる機械学習",
            "isbn": isbn,
            "author": ["有賀康顕", "中山心太", "西林孝"],
            "google_books_url": "test_google_books_url",
            "image_url": None,
        }

    monkeypatch.setattr(
        GoogleBooksRepository, "search_book_by_isbn", mock_search_book_by_isbn
    )

    user: User = {
        "user_id": "U03B49AKZV4",
        "user_name": "永和太郎",
        "department": "finance",
        "job_type": "engineer",
        "age_range": "60",
        "updated_at": None,
    }

    logger = getLogger()
    book = recommend(logger, user)

    assert book["title"] == "仕事ではじめる機械学習"
    assert book["isbn"] == "9784873118253"
    assert book["author"] == ["有賀康顕", "中山心太", "西林孝"]
    assert book["image_url"] is None
    assert book["google_books_url"] == "test_google_books_url"


def test_モジュール内で例外が発生した場合は返値はNoneであること(monkeypatch):  # pylint: disable=invalid-name
    def mock_search_book_by_isbn(_, __):
        raise Exception("dummy exception")

    monkeypatch.setattr(
        GoogleBooksRepository, "search_book_by_isbn", mock_search_book_by_isbn
    )

    user: User = {
        "user_id": "U03B49AKZV4",
        "user_name": "永和太郎",
        "department": "finance",
        "job_type": "engineer",
        "age_range": "60",
        "updated_at": None,
    }

    logger = getLogger()
    book = recommend(logger, user)

    assert book is None
