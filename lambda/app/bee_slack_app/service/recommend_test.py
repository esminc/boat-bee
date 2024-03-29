# pylint: disable=non-ascii-name
# pylint: disable=invalid-name

from bee_slack_app.model import User
from bee_slack_app.repository.book_repository import BookRepository
from bee_slack_app.repository.recommend_book_repository import RecommendBookRepository
from bee_slack_app.repository.suggested_book_repository import SuggestedBookRepository
from bee_slack_app.service.recommend import recommend
from bee_slack_app.utils import datetime


def test_おすすめの本の情報を取得できること(monkeypatch):
    def mock_recommend_book_repository_fetch(_, __):
        return {
            "book_recommendations": [
                {"ml_model_name": "ml-a", "isbn": "1234567890123"}
            ],
            "created_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(
        RecommendBookRepository, "fetch", mock_recommend_book_repository_fetch
    )

    def mock_book_repository_fetch(_, isbn):
        return {
            "title": "仕事ではじめる機械学習",
            "isbn": isbn,
            "author": "有賀康顕,中山心太,西林孝",
            "url": "test_book_url",
            "image_url": "test_image_url",
            "description": "test_description",
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(BookRepository, "fetch", mock_book_repository_fetch)

    def mock_suggested_book_repository_get(
        _, *, user_id: str, isbn: str, ml_model: str
    ):
        return {
            "user_id": user_id,
            "isbn": isbn,
            "ml_model": ml_model,
            "interested": True,
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(
        SuggestedBookRepository, "fetch", mock_suggested_book_repository_get
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

    result = recommend(user)

    recommended_books = result["recommended_books"]

    assert recommended_books[0]["title"] == "仕事ではじめる機械学習"
    assert recommended_books[0]["isbn"] == "1234567890123"
    assert recommended_books[0]["author"] == "有賀康顕,中山心太,西林孝"
    assert recommended_books[0]["image_url"] == "test_image_url"
    assert recommended_books[0]["url"] == "test_book_url"
    assert recommended_books[0]["description"] == "test_description"
    assert recommended_books[0]["ml_model"] == "ml-a"
    assert recommended_books[0]["interested"] is True
    assert recommended_books[0]["updated_at"] == "2022-04-01T00:00:00+09:00"

    assert result["created_at"] == "2022-04-01T00:00:00+09:00"


def test_おすすめの本が取得できなかったらNoneを返すこと(monkeypatch):
    def mock_recommend_book_repository_fetch(_, __):
        return None

    monkeypatch.setattr(
        RecommendBookRepository, "fetch", mock_recommend_book_repository_fetch
    )

    def mock_book_repository_fetch(_, isbn):
        return {
            "title": "仕事ではじめる機械学習",
            "isbn": isbn,
            "author": "有賀康顕,中山心太,西林孝",
            "url": "test_book_url",
            "image_url": "test_image_url",
            "description": "test_description",
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(BookRepository, "fetch", mock_book_repository_fetch)

    def mock_suggested_book_repository_get(
        _, *, user_id: str, isbn: str, ml_model: str
    ):
        return {
            "user_id": user_id,
            "isbn": isbn,
            "ml_model": ml_model,
            "interested": True,
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(
        SuggestedBookRepository, "fetch", mock_suggested_book_repository_get
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

    assert recommended_books is None


def test_おすすめの本の情報がNoneのケース(monkeypatch):
    def mock_recommend_book_repository_fetch(_, __):
        return {
            "book_recommendations": [
                {"ml_model_name": "ml-a", "isbn": "1234567890123"}
            ],
            "created_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(
        RecommendBookRepository, "fetch", mock_recommend_book_repository_fetch
    )

    def mock_book_repository_fetch(_, __):
        return None

    monkeypatch.setattr(BookRepository, "fetch", mock_book_repository_fetch)

    def mock_suggested_book_repository_get(
        _, *, user_id: str, isbn: str, ml_model: str
    ):
        return {
            "user_id": user_id,
            "isbn": isbn,
            "ml_model": ml_model,
            "interested": True,
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(
        SuggestedBookRepository, "fetch", mock_suggested_book_repository_get
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

    result = recommend(user)

    assert result is None


def test_おすすめ本が未登録の場合は登録すること(mocker):

    mock_recommend_book_repository_fetch = mocker.patch.object(
        RecommendBookRepository, "fetch"
    )
    mock_recommend_book_repository_fetch.return_value = {
        "book_recommendations": [{"ml_model_name": "ml-a", "isbn": "1234567890123"}],
        "created_at": "2022-04-01T00:00:00+09:00",
    }

    def mock_book_repository_fetch(_, isbn):
        return {
            "title": "仕事ではじめる機械学習",
            "isbn": isbn,
            "author": "有賀康顕,中山心太,西林孝",
            "url": "test_book_url",
            "image_url": "test_image_url",
            "description": "test_description",
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

    mocker.patch.object(BookRepository, "fetch", mock_book_repository_fetch)

    mock_suggested_book_repository_get = mocker.patch.object(
        SuggestedBookRepository, "fetch"
    )
    mock_suggested_book_repository_get.return_value = None

    mock_suggested_book_repository_create = mocker.patch.object(
        SuggestedBookRepository, "put"
    )

    mocker.patch.object(datetime, "now").return_value = "2022-04-01T00:00:00+09:00"

    user: User = {
        "user_id": "U03B49AKZV4",
        "user_name": "永和太郎",
        "department": "finance",
        "job_type": "engineer",
        "age_range": "60",
        "updated_at": None,
        "post_review_count": 1,
    }

    recommend(user)

    assert mock_suggested_book_repository_create.call_count == 1

    args, _ = mock_suggested_book_repository_create.call_args

    assert args[0]["user_id"] == "U03B49AKZV4"
    assert args[0]["isbn"] == "1234567890123"
    assert args[0]["ml_model"] == "ml-a"
    assert args[0]["interested"] is False
    assert args[0]["updated_at"] == "2022-04-01T00:00:00+09:00"


def test_書影が取得できない場合に書影にNone返値に設定されること(monkeypatch):
    def mock_recommend_book_repository_fetch(_, __):
        return {
            "book_recommendations": [
                {"ml_model_name": "ml-a", "isbn": "1234567890123"}
            ],
            "created_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(
        RecommendBookRepository, "fetch", mock_recommend_book_repository_fetch
    )

    def mock_book_repository_fetch(_, isbn):
        return {
            "title": "仕事ではじめる機械学習",
            "isbn": isbn,
            "author": "有賀康顕,中山心太,西林孝",
            "url": "test_book_url",
            "image_url": None,
            "description": "test_description",
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(BookRepository, "fetch", mock_book_repository_fetch)

    def mock_suggested_book_repository_get(
        _, *, user_id: str, isbn: str, ml_model: str
    ):
        return {
            "user_id": user_id,
            "isbn": isbn,
            "ml_model": ml_model,
            "interested": True,
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(
        SuggestedBookRepository, "fetch", mock_suggested_book_repository_get
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

    result = recommend(user)

    recommended_books = result["recommended_books"]

    assert recommended_books[0]["title"] == "仕事ではじめる機械学習"
    assert recommended_books[0]["isbn"] == "1234567890123"
    assert recommended_books[0]["author"] == "有賀康顕,中山心太,西林孝"
    assert recommended_books[0]["image_url"] is None
    assert recommended_books[0]["url"] == "test_book_url"
    assert recommended_books[0]["description"] == "test_description"
    assert recommended_books[0]["ml_model"] == "ml-a"
    assert recommended_books[0]["interested"] is True
    assert recommended_books[0]["updated_at"] == "2022-04-01T00:00:00+09:00"

    assert result["created_at"] == "2022-04-01T00:00:00+09:00"


def test_モジュール内で例外が発生した場合は返値はNoneであること(monkeypatch):
    def mock_recommend_book_repository_fetch(_, __):
        return {
            "book_recommendations": [
                {"ml_model_name": "ml-a", "isbn": "1234567890123"}
            ],
            "created_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(
        RecommendBookRepository, "fetch", mock_recommend_book_repository_fetch
    )

    def mock_book_repository_fetch(_):
        raise Exception("dummy exception")

    monkeypatch.setattr(BookRepository, "fetch", mock_book_repository_fetch)

    def mock_suggested_book_repository_get(
        _, *, user_id: str, isbn: str, ml_model: str
    ):
        return {
            "user_id": user_id,
            "isbn": isbn,
            "ml_model": ml_model,
            "interested": True,
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(
        SuggestedBookRepository, "fetch", mock_suggested_book_repository_get
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

    result = recommend(user)

    assert result is None


def test_複数のおすすめの本の情報を取得できること(monkeypatch):
    def mock_recommend_book_repository_fetch(_, __):
        return {
            "book_recommendations": [
                {"ml_model_name": "ml-a", "isbn": "1234567890123"},
                {"ml_model_name": "ml-b", "isbn": "9876543221098"},
            ],
            "created_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(
        RecommendBookRepository, "fetch", mock_recommend_book_repository_fetch
    )

    def mock_book_repository_fetch(_, isbn):
        if isbn == "1234567890123":
            book = {
                "title": "test_title_1",
                "isbn": isbn,
                "author": "test_authors_1",
                "url": "test_book_url_1",
                "image_url": "test_image_url_1",
                "description": "test_description_1",
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        elif isbn == "9876543221098":
            book = {
                "title": "test_title_2",
                "isbn": isbn,
                "author": "test_authors_2",
                "url": "test_book_url_2",
                "image_url": "test_image_url_2",
                "description": "test_description_2",
                "updated_at": "2022-04-02T00:00:00+09:00",
            }
        return book

    monkeypatch.setattr(BookRepository, "fetch", mock_book_repository_fetch)

    def mock_suggested_book_repository_get(
        _, *, user_id: str, isbn: str, ml_model: str
    ):
        if isbn == "1234567890123":
            return {
                "user_id": user_id,
                "isbn": isbn,
                "ml_model": ml_model,
                "interested": True,
                "updated_at": "2022-04-01T00:00:00+09:00",
            }
        return {
            "user_id": user_id,
            "isbn": isbn,
            "ml_model": ml_model,
            "interested": False,
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

    monkeypatch.setattr(
        SuggestedBookRepository, "fetch", mock_suggested_book_repository_get
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

    result = recommend(user)

    recommended_books = result["recommended_books"]

    assert recommended_books[0]["title"] == "test_title_1"
    assert recommended_books[0]["isbn"] == "1234567890123"
    assert recommended_books[0]["author"] == "test_authors_1"
    assert recommended_books[0]["image_url"] == "test_image_url_1"
    assert recommended_books[0]["url"] == "test_book_url_1"
    assert recommended_books[0]["description"] == "test_description_1"
    assert recommended_books[0]["ml_model"] == "ml-a"
    assert recommended_books[0]["interested"] is True
    assert recommended_books[0]["updated_at"] == "2022-04-01T00:00:00+09:00"

    assert recommended_books[1]["title"] == "test_title_2"
    assert recommended_books[1]["isbn"] == "9876543221098"
    assert recommended_books[1]["author"] == "test_authors_2"
    assert recommended_books[1]["image_url"] == "test_image_url_2"
    assert recommended_books[1]["url"] == "test_book_url_2"
    assert recommended_books[1]["description"] == "test_description_2"
    assert recommended_books[1]["ml_model"] == "ml-b"
    assert recommended_books[1]["interested"] is False
    assert recommended_books[1]["updated_at"] == "2022-04-02T00:00:00+09:00"

    assert result["created_at"] == "2022-04-01T00:00:00+09:00"
