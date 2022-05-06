from bee_slack_app.model.user import User
from bee_slack_app.service.user import add_user


def test_ユーザ情報を登録できること(self, monkeypatch):
    def mock_add_user(self, _):
        user = {
            "user_id": "user_id_0",
            "user_name": "えいわ　金融１",
            "department": "fin",
            "job_type": "engineer",
            "age_range": "20",
        }
        return user

    monkeypatch.setattr(User, "create", mock_add_user)

    user = add_user()

    assert user[0]["user_id"] == "user_id_0"
    assert user[0]["user_name"] == "えいわ　金融１"
    assert user[0]["department"] == "fin"
    assert user[0]["job_type"] == "engineer"
    assert user[0]["age_range"] == "20"
