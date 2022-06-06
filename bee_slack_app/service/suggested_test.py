# pylint: disable=non-ascii-name

from bee_slack_app.repository.suggested_book_repository import SuggestedBookRepository
from bee_slack_app.service.suggested import get_suggested


def test_おすすめ本の情報を取得を取得できること(monkeypatch):
    def mock_suggested_repository_get(_, **__):
        return {
            "user_id": "test_user_id",
            "isbn": "1234567890123",
            "ml_model": "test_ml_model",
            "interested": False,
            "updated_at": "2022-05-02T16:43:25+09:00",
        }

    monkeypatch.setattr(SuggestedBookRepository, "get", mock_suggested_repository_get)

    suggested = get_suggested(
        user_id="test_user_id", isbn="1234567890123", ml_model="test_ml_model"
    )
    print(suggested)

    assert suggested["user_id"] == "test_user_id"
    assert suggested["isbn"] == "1234567890123"
    assert suggested["ml_model"] == "test_ml_model"
    assert suggested["interested"] is False
    assert suggested["updated_at"] == "2022-05-02T16:43:25+09:00"


def test_おすすめ本の情報がない場合はノンを返す(monkeypatch):
    def mock_suggested_repository_get(_, **__):
        return None

    monkeypatch.setattr(SuggestedBookRepository, "get", mock_suggested_repository_get)

    suggested = get_suggested(
        user_id="test_user_id", isbn="1234567890123", ml_model="test_ml_model"
    )

    assert suggested is None
