# pylint: disable=non-ascii-name

from bee_slack_app.repository.recommend_book_repository import RecommendBookRepository


def test_おすすめ本を取得できること(mocker):
    mocker.patch.object(
        RecommendBookRepository,
        "_load_recommend_book_dict",
        return_value={"user_id_0": "1234567890123", "user_id_1": "1234567890456"},
    )

    recommend_book_repository = RecommendBookRepository()

    recommend_book_isbn = recommend_book_repository.fetch("user_id_0")

    assert recommend_book_isbn == "1234567890123"


def test_おすすめ本の取得で存在しないユーザIDに対してはNoneを返すこと(mocker):  # pylint: disable=invalid-name
    mocker.patch.object(
        RecommendBookRepository,
        "_load_recommend_book_dict",
        return_value={"user_id_0": "1234567890123", "user_id_1": "1234567890456"},
    )

    recommend_book_repository = RecommendBookRepository()

    recommend_book_isbn = recommend_book_repository.fetch("user_id_not_exist")

    assert recommend_book_isbn is None
