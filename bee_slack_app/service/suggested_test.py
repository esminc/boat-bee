# pylint: disable=non-ascii-name
# pylint: disable=invalid-name
# pylint: disable=no-self-use

from bee_slack_app.repository.suggested_book_repository import SuggestedBookRepository
from bee_slack_app.service.suggested import get_is_interested


class Test_get_is_interested:
    def test_おすすめ本の情報を取得を取得できること(self, monkeypatch):
        def mock_suggested_repository_get(_, **__):
            return {
                "user_id": "test_user_id",
                "isbn": "1234567890123",
                "ml_model": "test_ml_model",
                "interested": False,
                "updated_at": "2022-05-02T16:43:25+09:00",
            }

        monkeypatch.setattr(
            SuggestedBookRepository, "get", mock_suggested_repository_get
        )

        result = get_is_interested(
            user_id="test_user_id", isbn="1234567890123", ml_model="test_ml_model"
        )
        assert result is False

    def test_おすすめ本の情報がない場合はNoneを返す(self, monkeypatch):
        def mock_suggested_repository_get(_, **__):
            return None

        monkeypatch.setattr(
            SuggestedBookRepository, "get", mock_suggested_repository_get
        )

        result = get_is_interested(
            user_id="test_user_id", isbn="1234567890123", ml_model="test_ml_model"
        )

        assert result is None
