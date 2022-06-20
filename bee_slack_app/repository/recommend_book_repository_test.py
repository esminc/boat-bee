# pylint: disable=non-ascii-name
# pylint: disable=invalid-name

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
            },
            "metadata": {
                "hoge": "hoge_value",
                "fuga": "fuga_value",
            },
        },
    )

    recommend_book_repository = RecommendBookRepository()

    recommend_book_isbn = recommend_book_repository.fetch("user_id_0")

    assert recommend_book_isbn == {
        "ML-a": "1234567890123",
        "ML-b": "2345678901234",
    }


def test_おすすめ本の取得で存在しないユーザIDに対してはNoneを返すこと(mocker):
    mocker.patch.object(
        RecommendBookRepository,
        "_load_recommend_info",
        return_value={
            "result": {"user_id_0": "1234567890123", "user_id_1": "1234567890456"},
            "metadata": {
                "hoge": "hoge_value",
                "fuga": "fuga_value",
            },
        },
    )

    recommend_book_repository = RecommendBookRepository()

    recommend_book_isbn = recommend_book_repository.fetch("user_id_not_exist")

    assert recommend_book_isbn is None


def test_ひとつのMLがNoneでもおすすめ本を取得できること(mocker):
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
            "metadata": {
                "hoge": "hoge_value",
                "fuga": "fuga_value",
            },
        },
    )

    recommend_book_repository = RecommendBookRepository()

    recommend_book_isbn = recommend_book_repository.fetch("user_id_0")

    assert recommend_book_isbn == {
        "ML-b": "2345678901234",
    }


def test_JSONのメタデータが辞書形式で取得できること(mocker):
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
            "metadata": {
                "hoge": "hoge_value",
                "fuga": "fuga_value",
            },
        },
    )

    recommend_book_repository = RecommendBookRepository()

    metadata = recommend_book_repository.fetch_metadata()

    assert isinstance(metadata, dict)
    assert metadata == {
        "hoge": "hoge_value",
        "fuga": "fuga_value",
    }
