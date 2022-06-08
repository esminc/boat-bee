# pylint: disable=non-ascii-name


from bee_slack_app.model.user import User
from bee_slack_app.repository.user_repository import UserRepository
from bee_slack_app.service.user import (
    add_user,
    get_all_user,
    get_user,
    get_users_posted_review,
)
from bee_slack_app.utils import datetime


def test_ユーザを登録できること(mocker):
    mock_user_repository_create = mocker.patch.object(UserRepository, "create")

    mocker.patch.object(datetime, "now").return_value = "2022-04-01T00:00:00+09:00"

    user: User = {
        "user_id": "U03B49AKZV4",
        "user_name": "永和太郎",
        "department": "finance",
        "job_type": "engineer",
        "age_range": "60",
        "updated_at": None,
        "post_review_count": 0,
    }

    add_user(user)

    args, _ = mock_user_repository_create.call_args

    assert args[0]["user_id"] == "U03B49AKZV4"
    assert args[0]["user_name"] == "永和太郎"
    assert args[0]["department"] == "finance"
    assert args[0]["job_type"] == "engineer"
    assert args[0]["age_range"] == "60"
    assert args[0]["updated_at"] == "2022-04-01T00:00:00+09:00"
    assert args[0]["post_review_count"] == 0


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

    user = get_user("test_user_id")

    assert user["user_id"] == "test_user_id"
    assert user["user_name"] == "北ノ庄　肇"
    assert user["department"] == "金融システム事業部"
    assert user["job_type"] == "営業職"
    assert user["age_range"] == "30"
    assert user["updated_at"] == "2022-05-02T16:43:25+09:00"


def test_全てのユーザー情報を取得できること(monkeypatch):
    def mock_user_repository_get_all(_):
        return [
            {
                "user_id": "test_user_id_0",
                "user_name": "永和　太郎",
                "department": "ＩＴＳ事業部",
                "job_type": "技術職",
                "age_range": "20",
                "updated_at": "2022-04-01T00:00:00+09:00",
            },
            {
                "user_id": "test_user_id_1",
                "user_name": "問屋町　花子",
                "department": "ＩＴＳ事業部",
                "job_type": "管理職",
                "age_range": "50",
                "updated_at": "2022-04-11T09:23:04+09:00",
            },
            {
                "user_id": "test_user_id_2",
                "user_name": "北ノ庄　肇",
                "department": "金融システム事業部",
                "job_type": "営業職",
                "age_range": "30",
                "updated_at": "2022-05-02T16:43:25+09:00",
            },
        ]

    monkeypatch.setattr(UserRepository, "get_all", mock_user_repository_get_all)

    users = get_all_user()

    assert len(users) == 3

    assert users[0]["user_id"] == "test_user_id_0"
    assert users[0]["user_name"] == "永和　太郎"
    assert users[0]["department"] == "ＩＴＳ事業部"
    assert users[0]["job_type"] == "技術職"
    assert users[0]["age_range"] == "20"
    assert users[0]["updated_at"] == "2022-04-01T00:00:00+09:00"

    assert users[1]["user_id"] == "test_user_id_1"
    assert users[1]["user_name"] == "問屋町　花子"
    assert users[1]["department"] == "ＩＴＳ事業部"
    assert users[1]["job_type"] == "管理職"
    assert users[1]["age_range"] == "50"
    assert users[1]["updated_at"] == "2022-04-11T09:23:04+09:00"

    assert users[2]["user_id"] == "test_user_id_2"
    assert users[2]["user_name"] == "北ノ庄　肇"
    assert users[2]["department"] == "金融システム事業部"
    assert users[2]["job_type"] == "営業職"
    assert users[2]["age_range"] == "30"
    assert users[2]["updated_at"] == "2022-05-02T16:43:25+09:00"


def test_全取得ではユーザー情報が無い場合に空のリストを返すこと(monkeypatch):
    def mock_user_repository_get_all(_):
        return []

    monkeypatch.setattr(UserRepository, "get_all", mock_user_repository_get_all)

    users = get_all_user()

    assert len(users) == 0


def test_全取得ではrepositoryの処理でエラーが発生した場合空のリストを返すこと(
    monkeypatch,
):  # pylint: disable=invalid-name
    def mock_user_repository_get_all(_):
        raise Exception("dummy exception")

    monkeypatch.setattr(UserRepository, "get_all", mock_user_repository_get_all)

    users = get_all_user()

    assert len(users) == 0


def test_ユーザー情報が無い場合にNoneを返すこと(monkeypatch):  # pylint: disable=invalid-name
    def mock_user_repository_get(_, __):
        return None

    monkeypatch.setattr(UserRepository, "get", mock_user_repository_get)

    user = get_user("test_user_id")

    assert user is None


def test_repositoryの処理でエラーが発生した場合Noneを返すこと(monkeypatch):  # pylint: disable=invalid-name
    def mock_user_repository_get(_):
        raise Exception("dummy exception")

    monkeypatch.setattr(UserRepository, "get", mock_user_repository_get)

    user = get_user("test_user_id")

    assert user is None


def test_レビューを投稿しているユーザを取得できること(monkeypatch):  # pylint: disable=invalid-name
    def mock_user_repository_get_by_posted_review(_):
        return [
            {
                "user_id": "test_user_id_0",
                "user_name": "永和　太郎",
                "department": "ＩＴＳ事業部",
                "job_type": "技術職",
                "age_range": "20",
                "updated_at": "2022-04-01T00:00:00+09:00",
            },
            {
                "user_id": "test_user_id_1",
                "user_name": "問屋町　花子",
                "department": "ＩＴＳ事業部",
                "job_type": "管理職",
                "age_range": "50",
                "updated_at": "2022-04-11T09:23:04+09:00",
            },
            {
                "user_id": "test_user_id_2",
                "user_name": "北ノ庄　肇",
                "department": "金融システム事業部",
                "job_type": "営業職",
                "age_range": "30",
                "updated_at": "2022-05-02T16:43:25+09:00",
            },
        ]

    monkeypatch.setattr(
        UserRepository,
        "get_by_posted_review",
        mock_user_repository_get_by_posted_review,
    )

    users = get_users_posted_review()

    assert len(users) == 3

    assert users[0]["user_id"] == "test_user_id_0"
    assert users[0]["user_name"] == "永和　太郎"
    assert users[0]["department"] == "ＩＴＳ事業部"
    assert users[0]["job_type"] == "技術職"
    assert users[0]["age_range"] == "20"
    assert users[0]["updated_at"] == "2022-04-01T00:00:00+09:00"

    assert users[1]["user_id"] == "test_user_id_1"
    assert users[1]["user_name"] == "問屋町　花子"
    assert users[1]["department"] == "ＩＴＳ事業部"
    assert users[1]["job_type"] == "管理職"
    assert users[1]["age_range"] == "50"
    assert users[1]["updated_at"] == "2022-04-11T09:23:04+09:00"

    assert users[2]["user_id"] == "test_user_id_2"
    assert users[2]["user_name"] == "北ノ庄　肇"
    assert users[2]["department"] == "金融システム事業部"
    assert users[2]["job_type"] == "営業職"
    assert users[2]["age_range"] == "30"
    assert users[2]["updated_at"] == "2022-05-02T16:43:25+09:00"
