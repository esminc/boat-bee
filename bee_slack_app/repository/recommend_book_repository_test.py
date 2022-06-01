# pylint: disable=non-ascii-name

from bee_slack_app.repository.recommend_book_repository import RecommendBookRepository


def test_複数のおすすめ本を取得できること(mocker):
    mocker.patch.object(
        RecommendBookRepository,
        "_load_recommend_info",
        return_value={
            "result": {
                "user_id_0": {
                    "ML-a": "1234567890123",
                    "ML-b": "2345678901234",
                },
                "user_id_1": {
                    "ML-a": "9876543210987",
                    "ML-b": "8765432109876",
                },
                "metadata": {"created_at": "2022-06-01T18:06:04+09:00"},
            }
        },
    )

    recommend_book_repository = RecommendBookRepository()

    recommend_book_isbn = recommend_book_repository.fetch("user_id_0")

    assert recommend_book_isbn == {
        "ML-a": "1234567890123",
        "ML-b": "2345678901234",
    }


def test_おすすめ本の取得で存在しないユーザIDに対してはNoneを返すこと(mocker):  # pylint: disable=invalid-name
    mocker.patch.object(
        RecommendBookRepository,
        "_load_recommend_info",
        return_value={
            "result": {"user_id_0": "1234567890123", "user_id_1": "1234567890456"},
            "metadata": {"created_at": "2022-06-01T18:06:04+09:00"},
        },
    )

    recommend_book_repository = RecommendBookRepository()

    recommend_book_isbn = recommend_book_repository.fetch("user_id_not_exist")

    assert recommend_book_isbn is None


def test_ひとつのMLがNoneでもおすすめ本を取得できること(mocker):  # pylint: disable=invalid-name
    mocker.patch.object(
        RecommendBookRepository,
        "_load_recommend_info",
        return_value={
            "result": {
                "user_id_0": {
                    "ML-b": "2345678901234",
                },
                "user_id_1": {
                    "ML-a": "9876543210987",
                    "ML-b": "8765432109876",
                },
            },
            "metadata": {"created_at": "2022-06-01T18:06:04+09:00"},
        },
    )

    recommend_book_repository = RecommendBookRepository()

    recommend_book_isbn = recommend_book_repository.fetch("user_id_0")

    assert recommend_book_isbn == {
        "ML-b": "2345678901234",
    }


def test_JSONの生成時刻が取得できること(mocker):
    mocker.patch.object(
        RecommendBookRepository,
        "_load_recommend_info",
        return_value={
            "result": {
                "user_id_0": {
                    "ML-a": "1234567890123",
                    "ML-b": "2345678901234",
                },
                "user_id_1": {
                    "ML-a": "9876543210987",
                    "ML-b": "8765432109876",
                },
            },
            "metadata": {"created_at": "2022-06-01T18:06:04+09:00"},
        },
    )

    recommend_book_repository = RecommendBookRepository()

    timestamp = recommend_book_repository.created_at()

    assert timestamp is not None
    assert timestamp == "2022-06-01T18:06:04+09:00"
