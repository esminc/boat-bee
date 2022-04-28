from bee_slack_app.model.user import User
from bee_slack_app.service.user import add_user


def test_ユーザ情報を登録できること(monkeypatch):
    def mock_add_user(arg):
        return [
            {
                "user_id": "user_id_0",
                "user_name": "えいわ　金融１",
                "department": "fin",
                "job_type": "engineer",
                "age_range": "20",
            },
        ]

    monkeypatch.setattr(UserProfile, "create", mock_add_user)

    user_info = add_user()

    assert user_info[0]["user_id"] == "user_id_0"
    assert user_info[0]["user_name"] == "えいわ　金融１"
    assert user_info[0]["department"] == "fin"
    assert user_info[0]["job_type"] == "engineer"
    assert user_info[0]["age_range"] == "20"
