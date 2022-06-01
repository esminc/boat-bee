# pylint: disable=non-ascii-name


from bee_slack_app.repository.user_repository import UserRepository
from bee_slack_app.service.user import user_service


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

    user = user_service.get_user("test_user_id")

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

    users = user_service.get_all_user()

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

    users = user_service.get_all_user()

    assert len(users) == 0


def test_全取得ではrepositoryの処理でエラーが発生した場合空のリストを返すこと(
    monkeypatch,
):  # pylint: disable=invalid-name
    def mock_user_repository_get_all(_):
        raise Exception("dummy exception")

    monkeypatch.setattr(UserRepository, "get_all", mock_user_repository_get_all)

    users = user_service.get_all_user()

    assert len(users) == 0


def test_ユーザー情報が無い場合にNoneを返すこと(monkeypatch):  # pylint: disable=invalid-name
    def mock_user_repository_get(_, __):
        return None

    monkeypatch.setattr(UserRepository, "get", mock_user_repository_get)

    user = user_service.get_user("test_user_id")

    assert user is None


def test_repositoryの処理でエラーが発生した場合Noneを返すこと(monkeypatch):  # pylint: disable=invalid-name
    def mock_user_repository_get(_):
        raise Exception("dummy exception")

    monkeypatch.setattr(UserRepository, "get", mock_user_repository_get)

    user = user_service.get_user("test_user_id")

    assert user is None
