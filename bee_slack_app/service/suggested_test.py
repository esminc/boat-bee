# pylint: disable=non-ascii-name

from bee_slack_app.repository.suggested_book_repository import SuggestedBookRepository
from bee_slack_app.service.suggested import get_suggested_status


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

    result = get_suggested_status(
        user_id="test_user_id", isbn="1234567890123", ml_model="test_ml_model"
    )
    assert result is False


def test_おすすめ本の情報がない場合はNoneを返す(monkeypatch):  # pylint: disable=invalid-name
    def mock_suggested_repository_get(_, **__):
        return None

    monkeypatch.setattr(SuggestedBookRepository, "get", mock_suggested_repository_get)

    result = get_suggested_status(
        user_id="test_user_id", isbn="1234567890123", ml_model="test_ml_model"
    )

    assert result is None
