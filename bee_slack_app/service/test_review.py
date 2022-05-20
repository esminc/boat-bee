# pylint: disable=non-ascii-name


from logging import getLogger

from bee_slack_app.repository.review_repository import ReviewRepository
from bee_slack_app.repository.user_repository import UserRepository
from bee_slack_app.service.review import get_review, get_reviews, post_review
from bee_slack_app.utils import datetime


def test_get_reviewでレビューを取得できること(monkeypatch):
    def mock_review_repository_get(_, **__):
        return {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

    monkeypatch.setattr(ReviewRepository, "get", mock_review_repository_get)

    def mock_user_repository_get(_, __):
        return {
            "user_id": "user_id_0",
            "department": "department_0",
            "job_type": "job_type_0",
            "age_range": "age_range_0",
            "updated_at": "2022-04-11T09:23:04+09:00",
            "user_name": "user_name_0",
        }

    monkeypatch.setattr(UserRepository, "get", mock_user_repository_get)

    review = get_review(logger=getLogger(), user_id="user_id_0", isbn="12345")

    assert review["user_id"] == "user_id_0"
    assert review["user_name"] == "user_name_0"
    assert review["isbn"] == "12345"
    assert review["book_title"] == "仕事ではじめる機械学習"
    assert review["score_for_me"] == "1"
    assert review["score_for_others"] == "5"
    assert review["review_comment"] == "とても良いです"
    assert review["book_image_url"] == "dummy_book_image_url_0"
    assert review["book_author"] == "dummy_book_author_0"
    assert review["book_url"] == "dummy_book_url_0"


def test_get_reviewで該当するユーザ情報がない場合はユーザ名としてユーザIDを返すこと(
    monkeypatch,
):  # pylint: disable=invalid-name
    def mock_review_repository_get(_, **__):
        return {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

    monkeypatch.setattr(ReviewRepository, "get", mock_review_repository_get)

    def mock_user_repository_get(_, __):
        return None

    monkeypatch.setattr(UserRepository, "get", mock_user_repository_get)

    review = get_review(logger=getLogger(), user_id="user_id_0", isbn="12345")

    assert review["user_id"] == "user_id_0"
    assert review["user_name"] == "user_id_0"


def test_get_reviewでreview_repositoryの処理でエラーが発生した場合Noneを返すこと(
    monkeypatch,
):  # pylint: disable=invalid-name
    def mock_review_repository_get(_, **__):
        raise Exception("dummy exception")

    monkeypatch.setattr(ReviewRepository, "get", mock_review_repository_get)

    def mock_user_repository_get(_, __):
        return {
            "user_id": "user_id_0",
            "department": "department_0",
            "job_type": "job_type_0",
            "age_range": "age_range_0",
            "updated_at": "2022-04-11T09:23:04+09:00",
            "user_name": "user_name_0",
        }

    monkeypatch.setattr(UserRepository, "get", mock_user_repository_get)

    review = get_review(logger=getLogger(), user_id="user_id_0", isbn="12345")

    assert review is None


def test_get_reviewでuser_repositoryの処理でエラーが発生した場合Noneを返すこと(
    monkeypatch,
):  # pylint: disable=invalid-name
    def mock_review_repository_get(_, **__):
        return {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

    monkeypatch.setattr(ReviewRepository, "get", mock_review_repository_get)

    def mock_user_repository_get(_, __):
        raise Exception("dummy exception")

    monkeypatch.setattr(UserRepository, "get", mock_user_repository_get)

    review = get_review(logger=getLogger(), user_id="user_id_0", isbn="12345")

    assert review is None


def test_get_reviewsでレビューを取得できること(monkeypatch):
    def mock_review_repository_get_some(_, **__):
        return {
            "items": [
                {
                    "user_id": "user_id_0",
                    "book_title": "仕事ではじめる機械学習",
                    "isbn": "12345",
                    "score_for_me": "1",
                    "score_for_others": "5",
                    "review_comment": "とても良いです",
                    "book_image_url": "dummy_book_image_url_0",
                    "book_author": "dummy_book_author_0",
                    "book_url": "dummy_book_url_0",
                },
                {
                    "user_id": "user_id_1",
                    "book_title": "仕事ではじめる機械学習",
                    "isbn": "12345",
                    "score_for_me": "3",
                    "score_for_others": "4",
                    "review_comment": "まあまあです",
                    "book_image_url": "dummy_book_image_url_1",
                    "book_author": "dummy_book_author_1",
                    "book_url": "dummy_book_url_1",
                },
                {
                    "user_id": "user_id_2",
                    "book_title": "Python チュートリアル",
                    "isbn": "67890",
                    "score_for_me": "2",
                    "score_for_others": "4",
                    "review_comment": "そこそこです",
                    "book_image_url": "dummy_book_image_url_2",
                    "book_author": "dummy_book_author_2",
                    "book_url": "dummy_book_url_2",
                },
            ],
            "last_key": None,
        }

    monkeypatch.setattr(ReviewRepository, "get_some", mock_review_repository_get_some)

    def mock_user_repository_get_all(_, **__):
        return [
            {
                "user_id": "user_id_0",
                "department": "department_0",
                "job_type": "job_type_0",
                "age_range": "age_range_0",
                "updated_at": "2022-04-11T09:23:04+09:00",
                "user_name": "user_name_0",
            },
            {
                "user_id": "user_id_1",
                "department": "department_1",
                "job_type": "job_type_1",
                "age_range": "age_range_1",
                "updated_at": "2022-04-12T09:23:04+09:00",
                "user_name": "user_name_1",
            },
            {
                "user_id": "user_id_2",
                "department": "department_2",
                "job_type": "job_type_2",
                "age_range": "age_range_2",
                "updated_at": "2022-04-12T09:23:04+09:00",
                "user_name": "user_name_2",
            },
        ]

    monkeypatch.setattr(UserRepository, "get_all", mock_user_repository_get_all)

    reviews = get_reviews(logger=getLogger(), limit=10, keys=[])["items"]

    assert len(reviews) == 3

    assert reviews[0]["user_id"] == "user_id_0"
    assert reviews[0]["user_name"] == "user_name_0"
    assert reviews[0]["isbn"] == "12345"
    assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[0]["score_for_me"] == "1"
    assert reviews[0]["score_for_others"] == "5"
    assert reviews[0]["review_comment"] == "とても良いです"
    assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
    assert reviews[0]["book_author"] == "dummy_book_author_0"
    assert reviews[0]["book_url"] == "dummy_book_url_0"

    assert reviews[1]["user_id"] == "user_id_1"
    assert reviews[1]["user_name"] == "user_name_1"
    assert reviews[1]["isbn"] == "12345"
    assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[1]["score_for_me"] == "3"
    assert reviews[1]["score_for_others"] == "4"
    assert reviews[1]["review_comment"] == "まあまあです"
    assert reviews[1]["book_image_url"] == "dummy_book_image_url_1"
    assert reviews[1]["book_author"] == "dummy_book_author_1"
    assert reviews[1]["book_url"] == "dummy_book_url_1"

    assert reviews[2]["user_id"] == "user_id_2"
    assert reviews[2]["user_name"] == "user_name_2"
    assert reviews[2]["isbn"] == "67890"
    assert reviews[2]["book_title"] == "Python チュートリアル"
    assert reviews[2]["score_for_me"] == "2"
    assert reviews[2]["score_for_others"] == "4"
    assert reviews[2]["review_comment"] == "そこそこです"
    assert reviews[2]["book_image_url"] == "dummy_book_image_url_2"
    assert reviews[2]["book_author"] == "dummy_book_author_2"
    assert reviews[2]["book_url"] == "dummy_book_url_2"


def test_get_reviewsで該当するユーザ情報がない場合はユーザ名としてユーザIDを返すこと(
    monkeypatch,
):  # pylint: disable=invalid-name
    def mock_review_repository_get_some(_, **__):
        return {
            "items": [
                {
                    "user_id": "user_id_0",
                    "book_title": "仕事ではじめる機械学習",
                    "isbn": "12345",
                    "score_for_me": "1",
                    "score_for_others": "5",
                    "review_comment": "とても良いです",
                    "book_image_url": "dummy_book_image_url_0",
                    "book_author": "dummy_book_author_0",
                    "book_url": "dummy_book_url_0",
                },
                {
                    "user_id": "user_id_1",
                    "book_title": "仕事ではじめる機械学習",
                    "isbn": "12345",
                    "score_for_me": "3",
                    "score_for_others": "4",
                    "review_comment": "まあまあです",
                    "book_image_url": "dummy_book_image_url_1",
                    "book_author": "dummy_book_author_1",
                    "book_url": "dummy_book_url_1",
                },
                {
                    "user_id": "user_id_2",
                    "book_title": "Python チュートリアル",
                    "isbn": "67890",
                    "score_for_me": "2",
                    "score_for_others": "4",
                    "review_comment": "そこそこです",
                    "book_image_url": "dummy_book_image_url_2",
                    "book_author": "dummy_book_author_2",
                    "book_url": "dummy_book_url_2",
                },
            ],
            "last_key": None,
        }

    monkeypatch.setattr(ReviewRepository, "get_some", mock_review_repository_get_some)

    def mock_user_repository_get_all(_, **__):
        return []

    monkeypatch.setattr(UserRepository, "get_all", mock_user_repository_get_all)

    reviews = get_reviews(logger=getLogger(), limit=10, keys=[])["items"]

    assert len(reviews) == 3

    assert reviews[0]["user_id"] == "user_id_0"
    assert reviews[0]["user_name"] == "user_id_0"
    assert reviews[0]["isbn"] == "12345"
    assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[0]["score_for_me"] == "1"
    assert reviews[0]["score_for_others"] == "5"
    assert reviews[0]["review_comment"] == "とても良いです"
    assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
    assert reviews[0]["book_author"] == "dummy_book_author_0"
    assert reviews[0]["book_url"] == "dummy_book_url_0"

    assert reviews[1]["user_id"] == "user_id_1"
    assert reviews[1]["user_name"] == "user_id_1"
    assert reviews[1]["isbn"] == "12345"
    assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[1]["score_for_me"] == "3"
    assert reviews[1]["score_for_others"] == "4"
    assert reviews[1]["review_comment"] == "まあまあです"
    assert reviews[1]["book_image_url"] == "dummy_book_image_url_1"
    assert reviews[1]["book_author"] == "dummy_book_author_1"
    assert reviews[1]["book_url"] == "dummy_book_url_1"

    assert reviews[2]["user_id"] == "user_id_2"
    assert reviews[2]["user_name"] == "user_id_2"
    assert reviews[2]["isbn"] == "67890"
    assert reviews[2]["book_title"] == "Python チュートリアル"
    assert reviews[2]["score_for_me"] == "2"
    assert reviews[2]["score_for_others"] == "4"
    assert reviews[2]["review_comment"] == "そこそこです"
    assert reviews[2]["book_image_url"] == "dummy_book_image_url_2"
    assert reviews[2]["book_author"] == "dummy_book_author_2"
    assert reviews[2]["book_url"] == "dummy_book_url_2"


def test_get_reviewsでreview_repositoryの処理でエラーが発生した場合Noneを返すこと(
    monkeypatch,
):  # pylint: disable=invalid-name
    def mock_review_repository_get_some(_, __):
        raise Exception("dummy exception")

    monkeypatch.setattr(UserRepository, "get_all", mock_review_repository_get_some)

    reviews = get_reviews(logger=getLogger(), limit=10, keys=[])

    assert reviews is None


def test_get_reviewsでuser_repositoryの処理でエラーが発生した場合Noneを返すこと(
    monkeypatch,
):  # pylint: disable=invalid-name
    def mock_user_repository_get_all(_, __):
        raise Exception("dummy exception")

    monkeypatch.setattr(ReviewRepository, "get", mock_user_repository_get_all)

    reviews = get_reviews(logger=getLogger(), limit=10, keys=[])

    assert reviews is None


def test_post_reviewでレビューを投稿できること(
    mocker,
):  # pylint: disable=invalid-name
    mock_review_repository_create = mocker.patch.object(ReviewRepository, "create")

    mocker.patch.object(datetime, "now").return_value = "2022-04-01T00:00:00+09:00"

    review = post_review(
        logger=getLogger(),
        review_contents={
            "user_id": "test_user_id",
            "isbn": "12345",
            "book_title": "本のタイトル",
            "score_for_me": "1",
            "score_for_others": "3",
            "review_comment": "レビューコメント",
            "book_image_url": "dummy_book_author",
            "book_author": "dummy_book_author",
            "book_url": "dummy_book_url",
        },
    )

    assert mock_review_repository_create.call_count == 1

    assert review["user_id"] == "test_user_id"
    assert review["isbn"] == "12345"
    assert review["book_title"] == "本のタイトル"
    assert review["score_for_me"] == "1"
    assert review["score_for_others"] == "3"
    assert review["review_comment"] == "レビューコメント"
    assert review["updated_at"] == "2022-04-01T00:00:00+09:00"
    assert review["book_image_url"] == "dummy_book_author"
    assert review["book_author"] == "dummy_book_author"
    assert review["book_url"] == "dummy_book_url"


def test_post_reviewでreview_repositoryの処理でエラーが発生した場合Noneを返すこと(
    mocker,
):  # pylint: disable=invalid-name
    mock_review_repository_create = mocker.patch.object(ReviewRepository, "create")
    mock_review_repository_create.side_effect = Exception("dummy exception")

    mocker.patch.object(datetime, "now").return_value = "2022-04-01T00:00:00+09:00"

    review = post_review(
        logger=getLogger(),
        review_contents={
            "user_id": "test_user_id",
            "isbn": "12345",
            "book_title": "本のタイトル",
            "score_for_me": "1",
            "score_for_others": "3",
            "review_comment": "レビューコメント",
            "book_image_url": "dummy_book_author",
            "book_author": "dummy_book_author",
            "book_url": "dummy_book_url",
        },
    )

    assert mock_review_repository_create.call_count == 1

    assert review is None


def test_get_reviewsでレビューを全件一括で取得できること(monkeypatch):
    def mock_review_repository_get_some(_, **__):
        return {
            "items": [
                {
                    "user_id": "user_id_0",
                    "book_title": "仕事ではじめる機械学習",
                    "isbn": "12345",
                    "score_for_me": "1",
                    "score_for_others": "5",
                    "review_comment": "とても良いです",
                    "book_image_url": "dummy_book_image_url_0",
                    "book_author": "dummy_book_author_0",
                    "book_url": "dummy_book_url_0",
                },
                {
                    "user_id": "user_id_1",
                    "book_title": "仕事ではじめる機械学習",
                    "isbn": "12345",
                    "score_for_me": "3",
                    "score_for_others": "4",
                    "review_comment": "まあまあです",
                    "book_image_url": "dummy_book_image_url_1",
                    "book_author": "dummy_book_author_1",
                    "book_url": "dummy_book_url_1",
                },
                {
                    "user_id": "user_id_2",
                    "book_title": "Python チュートリアル",
                    "isbn": "67890",
                    "score_for_me": "2",
                    "score_for_others": "4",
                    "review_comment": "そこそこです",
                    "book_image_url": "dummy_book_image_url_2",
                    "book_author": "dummy_book_author_2",
                    "book_url": "dummy_book_url_2",
                },
            ],
            "last_key": None,
        }

    monkeypatch.setattr(ReviewRepository, "get_some", mock_review_repository_get_some)

    def mock_user_repository_get_all(_, **__):
        return [
            {
                "user_id": "user_id_0",
                "department": "department_0",
                "job_type": "job_type_0",
                "age_range": "age_range_0",
                "updated_at": "2022-04-11T09:23:04+09:00",
                "user_name": "user_name_0",
            },
            {
                "user_id": "user_id_1",
                "department": "department_1",
                "job_type": "job_type_1",
                "age_range": "age_range_1",
                "updated_at": "2022-04-12T09:23:04+09:00",
                "user_name": "user_name_1",
            },
            {
                "user_id": "user_id_2",
                "department": "department_2",
                "job_type": "job_type_2",
                "age_range": "age_range_2",
                "updated_at": "2022-04-12T09:23:04+09:00",
                "user_name": "user_name_2",
            },
        ]

    monkeypatch.setattr(UserRepository, "get_all", mock_user_repository_get_all)

    reviews = get_reviews(logger=getLogger(), limit=[], keys=[])["items"]

    assert len(reviews) == 3

    assert reviews[0]["user_id"] == "user_id_0"
    assert reviews[0]["user_name"] == "user_name_0"
    assert reviews[0]["isbn"] == "12345"
    assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[0]["score_for_me"] == "1"
    assert reviews[0]["score_for_others"] == "5"
    assert reviews[0]["review_comment"] == "とても良いです"
    assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
    assert reviews[0]["book_author"] == "dummy_book_author_0"
    assert reviews[0]["book_url"] == "dummy_book_url_0"

    assert reviews[1]["user_id"] == "user_id_1"
    assert reviews[1]["user_name"] == "user_name_1"
    assert reviews[1]["isbn"] == "12345"
    assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[1]["score_for_me"] == "3"
    assert reviews[1]["score_for_others"] == "4"
    assert reviews[1]["review_comment"] == "まあまあです"
    assert reviews[1]["book_image_url"] == "dummy_book_image_url_1"
    assert reviews[1]["book_author"] == "dummy_book_author_1"
    assert reviews[1]["book_url"] == "dummy_book_url_1"

    assert reviews[2]["user_id"] == "user_id_2"
    assert reviews[2]["user_name"] == "user_name_2"
    assert reviews[2]["isbn"] == "67890"
    assert reviews[2]["book_title"] == "Python チュートリアル"
    assert reviews[2]["score_for_me"] == "2"
    assert reviews[2]["score_for_others"] == "4"
    assert reviews[2]["review_comment"] == "そこそこです"
    assert reviews[2]["book_image_url"] == "dummy_book_image_url_2"
    assert reviews[2]["book_author"] == "dummy_book_author_2"
    assert reviews[2]["book_url"] == "dummy_book_url_2"
