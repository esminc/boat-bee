# pylint: disable=non-ascii-name

from logging import getLogger

from bee_slack_app.repository.user_repository import UserRepository
from bee_slack_app.service.user import get_user


def test_ユーザー情報を取得できること(monkeypatch):
    def mock_user_repository_get(_, __):
        return {
            "user_id": "test_user_id",
            "user_name": "北ノ庄　肇",
            "department": "金融システム事業部",
            "job_type": "営業職",
            "age_range": "30",
            "updated_at": "2022-05-02T16:43:25+09:00",
        }

    monkeypatch.setattr(UserRepository, "get", mock_user_repository_get)

    user = get_user(getLogger(), "test_user_id")

    assert user["user_id"] == "test_user_id"
    assert user["user_name"] == "北ノ庄　肇"
    assert user["department"] == "金融システム事業部"
    assert user["job_type"] == "営業職"
    assert user["age_range"] == "30"
    assert user["updated_at"] == "2022-05-02T16:43:25+09:00"


def test_ユーザー情報が無い場合にNoneを返すこと(monkeypatch):  # pylint: disable=invalid-name
    def mock_user_repository_get(_, __):
        return None

    monkeypatch.setattr(UserRepository, "get", mock_user_repository_get)

    user = get_user(getLogger(), "test_user_id")

    assert user is None


def test_repositoryの処理でエラーが発生した場合Noneを返すこと(monkeypatch):  # pylint: disable=invalid-name
    def mock_user_repository_get(_):
        raise Exception("dummy exception")

    monkeypatch.setattr(UserRepository, "get", mock_user_repository_get)

    user = get_user(getLogger(), "test_user_id")

    assert user is None
