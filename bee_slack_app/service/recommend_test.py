# pylint: disable=non-ascii-name
# pylint: disable=invalid-name

from bee_slack_app.model import User
from bee_slack_app.repository.google_books_repository import GoogleBooksRepository
from bee_slack_app.repository.recommend_book_repository import RecommendBookRepository
from bee_slack_app.service.recommend import created_at, recommend


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
        "post_review_count": 1,
    }

    recommended_books = recommend(user)

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
        "post_review_count": 1,
    }

    recommended_books = recommend(user)

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
        "post_review_count": 1,
    }

    recommended_books = recommend(user)

    assert len(recommended_books) == 0


def test_書影が取得できない場合に書影にNone返値に設定されること(monkeypatch):  # pylint: disable=invalid-name
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
        "post_review_count": 1,
    }

    recommended_books = recommend(user)

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
        "post_review_count": 1,
    }

    book = recommend(user)

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
        "post_review_count": 1,
    }

    recommended_books = recommend(user)

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


def test_おすすめ情報の生成時刻を取得できること(monkeypatch):
    def mock_recommend_book_repository_fetch_metadata(_):
        return {"created_at": "2022/04/01 00:00:00"}

    monkeypatch.setattr(
        RecommendBookRepository,
        "fetch_metadata",
        mock_recommend_book_repository_fetch_metadata,
    )

    timestamp = created_at()

    assert timestamp == "2022/04/01 00:00:00"


def test_メタデータが存在しない場合はNoneが返ること(monkeypatch):
    def mock_recommend_book_repository_fetch_metadata(_):
        return None

    monkeypatch.setattr(
        RecommendBookRepository,
        "fetch_metadata",
        mock_recommend_book_repository_fetch_metadata,
    )

    timestamp = created_at()

    assert timestamp is None


def test_メタデータにタイムスタンプ情報が存在しない場合はNoneが返ること(monkeypatch):
    def mock_recommend_book_repository_fetch_metadata(_):
        return {
            "hoge": "hoge_value",
            "fuga": "fuga_value",
        }

    monkeypatch.setattr(
        RecommendBookRepository,
        "fetch_metadata",
        mock_recommend_book_repository_fetch_metadata,
    )

    timestamp = created_at()

    assert timestamp is None


def test_メタデータ取得中にエラーが発生した場合はNoneが返ること(monkeypatch):
    def mock_recommend_book_repository_fetch_metadata(_):
        raise Exception("dummy exception")

    monkeypatch.setattr(
        RecommendBookRepository,
        "fetch_metadata",
        mock_recommend_book_repository_fetch_metadata,
    )

    timestamp = created_at()

    assert timestamp is None
