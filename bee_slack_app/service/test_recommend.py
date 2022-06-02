# pylint: disable=non-ascii-name

from logging import getLogger

from bee_slack_app.model.user import User
from bee_slack_app.repository.google_books_repository import GoogleBooksRepository
from bee_slack_app.repository.recommend_book_repository import RecommendBookRepository
from bee_slack_app.service.recommend import recommend


def test_おすすめの本の情報を取得できること(monkeypatch):
    def mock_recommend_book_repository_fetch(_, __):
        return {"ml-a": "1234567890123"}

    monkeypatch.setattr(
        RecommendBookRepository, "fetch", mock_recommend_book_repository_fetch
    )

    def mock_search_book_by_isbn(_, isbn):
        return {
            "title": "仕事ではじめる機械学習",
            "isbn": isbn,
            "authors": ["有賀康顕", "中山心太", "西林孝"],
            "google_books_url": "test_google_books_url",
            "image_url": "test_image_url",
            "description": "test_description",
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
    recommended_books = recommend(logger, user)

    # タプルの1番目は、本情報。２番目はモデル情報が格納されている。
    assert recommended_books[0][0]["title"] == "仕事ではじめる機械学習"
    assert recommended_books[0][0]["isbn"] == "1234567890123"
    assert recommended_books[0][0]["authors"] == ["有賀康顕", "中山心太", "西林孝"]
    assert recommended_books[0][0]["image_url"] == "test_image_url"
    assert recommended_books[0][0]["google_books_url"] == "test_google_books_url"
    assert recommended_books[0][0]["description"] == "test_description"
    assert recommended_books[0][1] == "ml-a"


def test_おすすめの本が取得できなかったら空のリストを返すこと(monkeypatch):  # pylint: disable=invalid-name
    def mock_recommend_book_repository_fetch(_, __):
        return []

    monkeypatch.setattr(
        RecommendBookRepository, "fetch", mock_recommend_book_repository_fetch
    )

    def mock_search_book_by_isbn(_, isbn):
        return {
            "title": "仕事ではじめる機械学習",
            "isbn": isbn,
            "authors": ["有賀康顕", "中山心太", "西林孝"],
            "google_books_url": "test_google_books_url",
            "image_url": "test_image_url",
            "description": "test_description",
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
    recommended_books = recommend(logger, user)

    assert len(recommended_books) == 0


def test_おすすめの本の情報がNoneのケース(monkeypatch):  # pylint: disable=invalid-name
    def mock_recommend_book_repository_fetch(_, __):
        return {"ml-a": "1234567890123"}

    monkeypatch.setattr(
        RecommendBookRepository, "fetch", mock_recommend_book_repository_fetch
    )

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
    recommended_books = recommend(logger, user)

    assert len(recommended_books) == 0


def test_おすすめ本の情報がNoneなら空のリストが返値に設定されること(monkeypatch):  # pylint: disable=invalid-name
    def mock_recommend_book_repository_fetch(_, __):
        return {"ml-a": "1234567890123"}

    monkeypatch.setattr(
        RecommendBookRepository, "fetch", mock_recommend_book_repository_fetch
    )

    def mock_search_book_by_isbn(_, isbn):
        return {
            "title": "仕事ではじめる機械学習",
            "isbn": isbn,
            "authors": ["有賀康顕", "中山心太", "西林孝"],
            "google_books_url": "test_google_books_url",
            "image_url": None,
            "description": "test_description",
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
    recommended_books = recommend(logger, user)

    # タプルの1番目は、本情報。２番目はモデル情報が格納されている。
    assert recommended_books[0][0]["title"] == "仕事ではじめる機械学習"
    assert recommended_books[0][0]["isbn"] == "1234567890123"
    assert recommended_books[0][0]["authors"] == ["有賀康顕", "中山心太", "西林孝"]
    assert recommended_books[0][0]["image_url"] is None
    assert recommended_books[0][0]["google_books_url"] == "test_google_books_url"
    assert recommended_books[0][0]["description"] == "test_description"
    assert recommended_books[0][1] == "ml-a"


def test_モジュール内で例外が発生した場合は返値は空のリストであること(monkeypatch):  # pylint: disable=invalid-name
    def mock_recommend_book_repository_fetch(_, __):
        return {"ml-a": "1234567890123"}

    monkeypatch.setattr(
        RecommendBookRepository, "fetch", mock_recommend_book_repository_fetch
    )

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

    assert len(book) == 0


def test_複数のおすすめの本の情報を取得できること(monkeypatch):
    def mock_recommend_book_repository_fetch(_, __):
        return {"ml-a": "1234567890123", "ml-b": "9876543221098"}

    monkeypatch.setattr(
        RecommendBookRepository, "fetch", mock_recommend_book_repository_fetch
    )

    def mock_search_book_by_isbn(_, isbn):
        if isbn == "1234567890123":
            book = {
                "title": "test_title_1",
                "isbn": isbn,
                "authors": "test_authors_1",
                "google_books_url": "test_google_books_url_1",
                "image_url": "test_image_url_1",
                "description": "test_description_1",
            }
        elif isbn == "9876543221098":
            book = {
                "title": "test_title_2",
                "isbn": isbn,
                "authors": "test_authors_2",
                "google_books_url": "test_google_books_url_2",
                "image_url": "test_image_url_2",
                "description": "test_description_2",
            }
        return book

    monkeypatch.setattr(
        GoogleBooksRepository, "search_book_by_isbn", mock_search_book_by_isbn
    )

    user: User = {
        "user_id": "test_user_id",
        "user_name": "test_user_name",
        "department": "test_department",
        "job_type": "test_job_type",
        "age_range": "test_age_range",
        "updated_at": None,
    }

    logger = getLogger()
    recommended_books = recommend(logger, user)

    # タプルの1番目は、本情報。２番目はモデル情報が格納されている。

    assert recommended_books[0][0]["title"] == "test_title_1"
    assert recommended_books[0][0]["isbn"] == "1234567890123"
    assert recommended_books[0][0]["authors"] == "test_authors_1"
    assert recommended_books[0][0]["image_url"] == "test_image_url_1"
    assert recommended_books[0][0]["google_books_url"] == "test_google_books_url_1"
    assert recommended_books[0][0]["description"] == "test_description_1"
    assert recommended_books[0][1] == "ml-a"

    assert recommended_books[1][0]["title"] == "test_title_2"
    assert recommended_books[1][0]["isbn"] == "9876543221098"
    assert recommended_books[1][0]["authors"] == "test_authors_2"
    assert recommended_books[1][0]["image_url"] == "test_image_url_2"
    assert recommended_books[1][0]["google_books_url"] == "test_google_books_url_2"
    assert recommended_books[1][0]["description"] == "test_description_2"
    assert recommended_books[1][1] == "ml-b"
