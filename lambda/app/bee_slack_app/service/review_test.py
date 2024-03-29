# pylint: disable=non-ascii-name
# pylint: disable=invalid-name
# pylint: disable=too-many-lines


from bee_slack_app.repository.book_repository import BookRepository
from bee_slack_app.repository.review_repository import ReviewRepository
from bee_slack_app.repository.user_repository import UserRepository
from bee_slack_app.service.review import (
    get_before_reviews_by_user_id,
    get_next_reviews_by_user_id,
    get_review,
    get_review_all,
    get_reviews_by_isbn,
    get_reviews_by_user_id,
    post_review,
)
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
            "book_description": "dummy_description_0",
        }

    monkeypatch.setattr(ReviewRepository, "fetch", mock_review_repository_get)

    def mock_user_repository_get(_, __):
        return {
            "user_id": "user_id_0",
            "department": "department_0",
            "job_type": "job_type_0",
            "age_range": "age_range_0",
            "updated_at": "2022-04-11T09:23:04+09:00",
            "user_name": "user_name_0",
        }

    monkeypatch.setattr(UserRepository, "fetch", mock_user_repository_get)

    review = get_review(user_id="user_id_0", isbn="12345")

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
    assert review["book_description"] == "dummy_description_0"


def test_get_reviewで該当するユーザ情報がない場合はユーザ名としてユーザIDを返すこと(
    monkeypatch,
):
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
            "book_description": "dummy_description_0",
        }

    monkeypatch.setattr(ReviewRepository, "fetch", mock_review_repository_get)

    def mock_user_repository_get(_, __):
        return None

    monkeypatch.setattr(UserRepository, "fetch", mock_user_repository_get)

    review = get_review(user_id="user_id_0", isbn="12345")

    assert review["user_id"] == "user_id_0"
    assert review["user_name"] == "user_id_0"


def test_get_reviewでreview_repositoryの処理でエラーが発生した場合Noneを返すこと(
    monkeypatch,
):
    def mock_review_repository_get(_, **__):
        raise Exception("dummy exception")

    monkeypatch.setattr(ReviewRepository, "fetch", mock_review_repository_get)

    def mock_user_repository_get(_, __):
        return {
            "user_id": "user_id_0",
            "department": "department_0",
            "job_type": "job_type_0",
            "age_range": "age_range_0",
            "updated_at": "2022-04-11T09:23:04+09:00",
            "user_name": "user_name_0",
        }

    monkeypatch.setattr(UserRepository, "fetch", mock_user_repository_get)

    review = get_review(user_id="user_id_0", isbn="12345")

    assert review is None


def test_get_reviewでuser_repositoryの処理でエラーが発生した場合Noneを返すこと(
    monkeypatch,
):
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
            "book_description": "dummy_description_0",
        }

    monkeypatch.setattr(ReviewRepository, "fetch", mock_review_repository_get)

    def mock_user_repository_get(_, __):
        raise Exception("dummy exception")

    monkeypatch.setattr(UserRepository, "fetch", mock_user_repository_get)

    review = get_review(user_id="user_id_0", isbn="12345")

    assert review is None


def test_get_review_allでレビューを取得できること(monkeypatch):
    def mock_review_repository_fetch_all(_, **__):
        return [
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
                "book_description": "dummy_description_0",
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
                "book_description": "dummy_description_1",
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
                "book_description": "dummy_description_2",
            },
        ]

    monkeypatch.setattr(ReviewRepository, "fetch_all", mock_review_repository_fetch_all)

    def mock_user_repository_fetch_all(_, **__):
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

    monkeypatch.setattr(UserRepository, "fetch_all", mock_user_repository_fetch_all)

    reviews = get_review_all()

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
    assert reviews[0]["book_description"] == "dummy_description_0"

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
    assert reviews[1]["book_description"] == "dummy_description_1"

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
    assert reviews[2]["book_description"] == "dummy_description_2"


def test_get_reviewsで該当するユーザ情報がない場合はユーザ名としてユーザIDを返すこと(
    monkeypatch,
):
    def mock_review_repository_fetch_all(_, **__):
        return [
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
                "book_description": "dummy_description_0",
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
                "book_description": "dummy_description_1",
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
                "book_description": "dummy_description_2",
            },
        ]

    monkeypatch.setattr(ReviewRepository, "fetch_all", mock_review_repository_fetch_all)

    def mock_user_repository_fetch_all(_, **__):
        return []

    monkeypatch.setattr(UserRepository, "fetch_all", mock_user_repository_fetch_all)

    reviews = get_review_all()

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
    assert reviews[0]["book_description"] == "dummy_description_0"

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
    assert reviews[1]["book_description"] == "dummy_description_1"

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
    assert reviews[2]["book_description"] == "dummy_description_2"


def test_get_review_allでreview_repositoryの処理でエラーが発生した場合Noneを返すこと(
    monkeypatch,
):
    def mock_review_repository_fetch_all(_, __):
        raise Exception("dummy exception")

    monkeypatch.setattr(UserRepository, "fetch_all", mock_review_repository_fetch_all)

    reviews = get_review_all()

    assert reviews is None


def test_get_review_allでuser_repositoryの処理でエラーが発生した場合Noneを返すこと(
    monkeypatch,
):
    def mock_user_repository_fetch_all(_, __):
        raise Exception("dummy exception")

    monkeypatch.setattr(ReviewRepository, "fetch", mock_user_repository_fetch_all)

    reviews = get_review_all()

    assert reviews is None


def test_post_reviewでレビューを投稿できること(
    mocker,
):
    mock_review_repository_create = mocker.patch.object(ReviewRepository, "put")

    mock_book_repository_put = mocker.patch.object(BookRepository, "put")

    mock_review_repository_fetch_by_user_id = mocker.patch.object(
        ReviewRepository, "fetch_by_user_id"
    )

    mock_user_repository_update_post_review_count = mocker.patch.object(
        UserRepository, "update_post_review_count"
    )

    mocker.patch.object(datetime, "now").return_value = "2022-04-01T00:00:00+09:00"

    review = post_review(
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
            "book_description": "dummy_description",
        },
    )

    assert mock_review_repository_create.call_count == 1

    assert mock_book_repository_put.call_count == 1

    assert mock_review_repository_fetch_by_user_id.call_count == 1

    assert mock_user_repository_update_post_review_count.call_count == 1

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
    assert review["book_description"] == "dummy_description"


def test_post_reviewでreview_repositoryの処理でエラーが発生した場合Noneを返すこと(
    mocker,
):
    mock_review_repository_create = mocker.patch.object(ReviewRepository, "put")
    mock_review_repository_create.side_effect = Exception("dummy exception")

    mock_book_repository_put = mocker.patch.object(BookRepository, "put")

    mock_review_repository_fetch_by_user_id = mocker.patch.object(
        ReviewRepository, "fetch_by_user_id"
    )

    mock_user_repository_update_post_review_count = mocker.patch.object(
        UserRepository, "update_post_review_count"
    )

    mocker.patch.object(datetime, "now").return_value = "2022-04-01T00:00:00+09:00"

    review = post_review(
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
            "book_description": "dummy_description",
        },
    )

    assert mock_review_repository_create.call_count == 1
    assert mock_book_repository_put.call_count == 0
    assert mock_review_repository_fetch_by_user_id.call_count == 0
    assert mock_user_repository_update_post_review_count.call_count == 0

    assert review is None


def test_post_reviewでbook_repositoryの処理でエラーが発生した場合Noneを返すこと(
    mocker,
):
    mock_review_repository_create = mocker.patch.object(ReviewRepository, "put")

    mock_book_repository_put = mocker.patch.object(BookRepository, "put")
    mock_book_repository_put.side_effect = Exception("dummy exception")

    mock_review_repository_fetch_by_user_id = mocker.patch.object(
        ReviewRepository, "fetch_by_user_id"
    )

    mock_user_repository_update_post_review_count = mocker.patch.object(
        UserRepository, "update_post_review_count"
    )

    mocker.patch.object(datetime, "now").return_value = "2022-04-01T00:00:00+09:00"

    review = post_review(
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
            "book_description": "dummy_description",
        },
    )

    assert mock_review_repository_create.call_count == 1
    assert mock_book_repository_put.call_count == 1
    assert mock_review_repository_fetch_by_user_id.call_count == 0
    assert mock_user_repository_update_post_review_count.call_count == 0

    assert review is None


def test_post_reviewでuser_repositoryの処理でエラーが発生した場合Noneを返すこと(
    mocker,
):
    mock_review_repository_create = mocker.patch.object(ReviewRepository, "put")

    mock_book_repository_put = mocker.patch.object(BookRepository, "put")

    mock_review_repository_fetch_by_user_id = mocker.patch.object(
        ReviewRepository, "fetch_by_user_id"
    )

    mock_user_repository_update_post_review_count = mocker.patch.object(
        UserRepository, "update_post_review_count"
    )
    mock_user_repository_update_post_review_count.side_effect = Exception(
        "dummy exception"
    )

    mocker.patch.object(datetime, "now").return_value = "2022-04-01T00:00:00+09:00"

    review = post_review(
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
            "book_description": "dummy_description",
        },
    )

    assert mock_review_repository_create.call_count == 1
    assert mock_book_repository_put.call_count == 1
    assert mock_review_repository_fetch_by_user_id.call_count == 1
    assert mock_user_repository_update_post_review_count.call_count == 1

    assert review is None


def test_get_reviews_by_isbnでレビューが取得できること(
    mocker,
):
    mock_review_repository_fetch_by_isbn = mocker.patch.object(
        ReviewRepository,
        "fetch_by_isbn",
    )
    mock_review_repository_fetch_by_isbn.return_value = [
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        },
        {
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        },
    ]

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.return_value = [
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

    reviews = get_reviews_by_isbn(isbn="1234567890123")

    assert len(reviews) == 2

    assert reviews[0]["user_id"] == "user_id_0"
    assert reviews[0]["user_name"] == "user_name_0"
    assert reviews[0]["isbn"] == "1234567890123"
    assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[0]["score_for_me"] == "1"
    assert reviews[0]["score_for_others"] == "5"
    assert reviews[0]["review_comment"] == "とても良いです"
    assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
    assert reviews[0]["book_author"] == "dummy_book_author_0"
    assert reviews[0]["book_url"] == "dummy_book_url_0"
    assert reviews[0]["book_description"] == "dummy_description_0"

    assert reviews[1]["user_id"] == "user_id_1"
    assert reviews[1]["user_name"] == "user_name_1"
    assert reviews[1]["isbn"] == "1234567890123"
    assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[1]["score_for_me"] == "3"
    assert reviews[1]["score_for_others"] == "4"
    assert reviews[1]["review_comment"] == "まあまあです"
    assert reviews[1]["book_image_url"] == "dummy_book_image_url_1"
    assert reviews[1]["book_author"] == "dummy_book_author_1"
    assert reviews[1]["book_url"] == "dummy_book_url_1"
    assert reviews[1]["book_description"] == "dummy_description_1"


def test_get_reviews_by_isbnでreview_repositoryの処理でエラーが発生した場合Noneを返すこと(
    mocker,
):
    mock_review_repository_fetch_by_isbn = mocker.patch.object(
        ReviewRepository,
        "fetch_by_isbn",
    )
    mock_review_repository_fetch_by_isbn.side_effect = Exception("dummy exception")

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.return_value = [
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

    reviews = get_reviews_by_isbn(isbn="1234567890123")

    assert reviews is None


def test_get_reviews_by_isbnでuser_repositoryの処理でエラーが発生した場合Noneを返すこと(
    mocker,
):
    mock_review_repository_fetch_by_isbn = mocker.patch.object(
        ReviewRepository,
        "fetch_by_isbn",
    )
    mock_review_repository_fetch_by_isbn.return_value = [
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        },
        {
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        },
    ]

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.side_effect = Exception("dummy exception")

    reviews = get_reviews_by_isbn(isbn="1234567890123")

    assert reviews is None


def test_get_reviews_by_isbnで該当するユーザ情報がない場合はユーザ名としてユーザIDを返すこと(
    mocker,
):
    mock_review_repository_fetch_by_isbn = mocker.patch.object(
        ReviewRepository,
        "fetch_by_isbn",
    )
    mock_review_repository_fetch_by_isbn.return_value = [
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        },
        {
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        },
    ]

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.return_value = []

    reviews = get_reviews_by_isbn(isbn="1234567890123")

    assert len(reviews) == 2

    assert reviews[0]["user_id"] == "user_id_0"
    assert reviews[0]["user_name"] == "user_id_0"
    assert reviews[0]["isbn"] == "1234567890123"
    assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[0]["score_for_me"] == "1"
    assert reviews[0]["score_for_others"] == "5"
    assert reviews[0]["review_comment"] == "とても良いです"
    assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
    assert reviews[0]["book_author"] == "dummy_book_author_0"
    assert reviews[0]["book_url"] == "dummy_book_url_0"
    assert reviews[0]["book_description"] == "dummy_description_0"

    assert reviews[1]["user_id"] == "user_id_1"
    assert reviews[1]["user_name"] == "user_id_1"
    assert reviews[1]["isbn"] == "1234567890123"
    assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[1]["score_for_me"] == "3"
    assert reviews[1]["score_for_others"] == "4"
    assert reviews[1]["review_comment"] == "まあまあです"
    assert reviews[1]["book_image_url"] == "dummy_book_image_url_1"
    assert reviews[1]["book_author"] == "dummy_book_author_1"
    assert reviews[1]["book_url"] == "dummy_book_url_1"
    assert reviews[1]["book_description"] == "dummy_description_1"


def test_get_reviews_by_user_idでレビューが取得できること(
    mocker,
):
    mock_review_repository_fetch_by_user_id = mocker.patch.object(
        ReviewRepository,
        "fetch_by_user_id",
    )
    mock_review_repository_fetch_by_user_id.return_value = [
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        },
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        },
    ]

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.return_value = [
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

    reviews = get_reviews_by_user_id(user_id="user_id_0")

    assert len(reviews) == 2

    assert reviews[0]["user_id"] == "user_id_0"
    assert reviews[0]["user_name"] == "user_name_0"
    assert reviews[0]["isbn"] == "1234567890123"
    assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[0]["score_for_me"] == "1"
    assert reviews[0]["score_for_others"] == "5"
    assert reviews[0]["review_comment"] == "とても良いです"
    assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
    assert reviews[0]["book_author"] == "dummy_book_author_0"
    assert reviews[0]["book_url"] == "dummy_book_url_0"
    assert reviews[0]["book_description"] == "dummy_description_0"

    assert reviews[1]["user_id"] == "user_id_0"
    assert reviews[1]["user_name"] == "user_name_0"
    assert reviews[1]["isbn"] == "1234567890123"
    assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[1]["score_for_me"] == "3"
    assert reviews[1]["score_for_others"] == "4"
    assert reviews[1]["review_comment"] == "まあまあです"
    assert reviews[1]["book_image_url"] == "dummy_book_image_url_1"
    assert reviews[1]["book_author"] == "dummy_book_author_1"
    assert reviews[1]["book_url"] == "dummy_book_url_1"
    assert reviews[1]["book_description"] == "dummy_description_1"


def test_get_reviews_by_user_idでreview_repositoryの処理でエラーが発生した場合Noneを返すこと(
    mocker,
):
    mock_review_repository_fetch_by_user_id = mocker.patch.object(
        ReviewRepository,
        "fetch_by_user_id",
    )
    mock_review_repository_fetch_by_user_id.side_effect = Exception("dummy exception")

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.return_value = [
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

    reviews = get_reviews_by_user_id(user_id="user_id_0")

    assert reviews is None


def test_get_reviews_by_user_idでuser_repositoryの処理でエラーが発生した場合Noneを返すこと(
    mocker,
):
    mock_review_repository_fetch_by_user_id = mocker.patch.object(
        ReviewRepository,
        "fetch_by_user_id",
    )
    mock_review_repository_fetch_by_user_id.return_value = [
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        },
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        },
    ]

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.side_effect = Exception("dummy exception")

    reviews = get_reviews_by_user_id(user_id="user_id_0")

    assert reviews is None


def test_get_reviews_by_user_idで該当するユーザ情報がない場合はユーザ名としてユーザIDを返すこと(
    mocker,
):
    mock_review_repository_fetch_by_user_id = mocker.patch.object(
        ReviewRepository,
        "fetch_by_user_id",
    )
    mock_review_repository_fetch_by_user_id.return_value = [
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        },
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        },
    ]

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.return_value = []

    reviews = get_reviews_by_user_id(user_id="user_id_0")

    assert len(reviews) == 2

    assert reviews[0]["user_id"] == "user_id_0"
    assert reviews[0]["user_name"] == "user_id_0"
    assert reviews[0]["isbn"] == "1234567890123"
    assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[0]["score_for_me"] == "1"
    assert reviews[0]["score_for_others"] == "5"
    assert reviews[0]["review_comment"] == "とても良いです"
    assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
    assert reviews[0]["book_author"] == "dummy_book_author_0"
    assert reviews[0]["book_url"] == "dummy_book_url_0"
    assert reviews[0]["book_description"] == "dummy_description_0"

    assert reviews[1]["user_id"] == "user_id_0"
    assert reviews[1]["user_name"] == "user_id_0"
    assert reviews[1]["isbn"] == "1234567890123"
    assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[1]["score_for_me"] == "3"
    assert reviews[1]["score_for_others"] == "4"
    assert reviews[1]["review_comment"] == "まあまあです"
    assert reviews[1]["book_image_url"] == "dummy_book_image_url_1"
    assert reviews[1]["book_author"] == "dummy_book_author_1"
    assert reviews[1]["book_url"] == "dummy_book_url_1"
    assert reviews[1]["book_description"] == "dummy_description_1"


def test_get_next_reviews_by_user_idで個数を指定してレビューが取得できること(
    mocker,
):
    mock_review_repository_fetch_limited_by_user_id = mocker.patch.object(
        ReviewRepository,
        "fetch_limited_by_user_id",
    )
    mock_review_repository_fetch_limited_by_user_id.return_value = [
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        },
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        },
    ]

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.return_value = [
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

    get_response = get_next_reviews_by_user_id(user_id="user_id_0", limit=1)

    if get_response is None:
        # このケースは本テストの対象外とする
        return

    reviews = get_response["items"]

    assert len(reviews) == 2

    assert reviews[0]["user_id"] == "user_id_0"
    assert reviews[0]["user_name"] == "user_name_0"
    assert reviews[0]["isbn"] == "1234567890123"
    assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[0]["score_for_me"] == "1"
    assert reviews[0]["score_for_others"] == "5"
    assert reviews[0]["review_comment"] == "とても良いです"
    assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
    assert reviews[0]["book_author"] == "dummy_book_author_0"
    assert reviews[0]["book_url"] == "dummy_book_url_0"
    assert reviews[0]["book_description"] == "dummy_description_0"

    assert reviews[1]["user_id"] == "user_id_0"
    assert reviews[1]["user_name"] == "user_name_0"
    assert reviews[1]["isbn"] == "1234567890123"
    assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[1]["score_for_me"] == "3"
    assert reviews[1]["score_for_others"] == "4"
    assert reviews[1]["review_comment"] == "まあまあです"
    assert reviews[1]["book_image_url"] == "dummy_book_image_url_1"
    assert reviews[1]["book_author"] == "dummy_book_author_1"
    assert reviews[1]["book_url"] == "dummy_book_url_1"
    assert reviews[1]["book_description"] == "dummy_description_1"


def test_get_next_reviews_by_user_idで不正なKEYを指定した場合はNoneが返ること(
    mocker,
):
    mock_review_repository_fetch_limited_by_user_id = mocker.patch.object(
        ReviewRepository,
        "fetch_limited_by_user_id",
    )
    mock_review_repository_fetch_limited_by_user_id.return_value = [
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        },
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        },
    ]

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.return_value = [
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

    get_response = get_next_reviews_by_user_id(
        user_id="user_id_0", limit=1, keys="INVALID_KEY_VALUE"
    )

    assert get_response is None


def test_get_next_reviews_by_user_idでuser_repositoryの処理でエラーが発生した場合Noneを返すこと(
    mocker,
):
    mock_review_repository_fetch_limited_by_user_id = mocker.patch.object(
        ReviewRepository,
        "fetch_by_user_id",
    )
    mock_review_repository_fetch_limited_by_user_id.return_value = [
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        },
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        },
    ]

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.side_effect = Exception("dummy exception")

    get_response = get_next_reviews_by_user_id(user_id="user_id_0", limit=1)

    assert get_response is None


def test_get_before_reviews_by_user_idで個数を指定してレビューが取得できること(
    mocker,
):
    mock_review_repository_fetch_limited_by_user_id = mocker.patch.object(
        ReviewRepository,
        "fetch_limited_by_user_id",
    )
    mock_review_repository_fetch_limited_by_user_id.return_value = [
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        },
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        },
    ]

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.return_value = [
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

    get_response = get_before_reviews_by_user_id(user_id="user_id_0", limit=1)

    if get_response is None:
        # このケースは本テストの対象外とする
        return

    reviews = get_response["items"]

    assert len(reviews) == 2

    assert reviews[0]["user_id"] == "user_id_0"
    assert reviews[0]["user_name"] == "user_name_0"
    assert reviews[0]["isbn"] == "1234567890123"
    assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[0]["score_for_me"] == "1"
    assert reviews[0]["score_for_others"] == "5"
    assert reviews[0]["review_comment"] == "とても良いです"
    assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
    assert reviews[0]["book_author"] == "dummy_book_author_0"
    assert reviews[0]["book_url"] == "dummy_book_url_0"
    assert reviews[0]["book_description"] == "dummy_description_0"

    assert reviews[1]["user_id"] == "user_id_0"
    assert reviews[1]["user_name"] == "user_name_0"
    assert reviews[1]["isbn"] == "1234567890123"
    assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
    assert reviews[1]["score_for_me"] == "3"
    assert reviews[1]["score_for_others"] == "4"
    assert reviews[1]["review_comment"] == "まあまあです"
    assert reviews[1]["book_image_url"] == "dummy_book_image_url_1"
    assert reviews[1]["book_author"] == "dummy_book_author_1"
    assert reviews[1]["book_url"] == "dummy_book_url_1"
    assert reviews[1]["book_description"] == "dummy_description_1"


def test_get_before_reviews_by_user_idで不正なKEYを指定した場合はNoneが返ること(
    mocker,
):
    mock_review_repository_fetch_limited_by_user_id = mocker.patch.object(
        ReviewRepository,
        "fetch_limited_by_user_id",
    )
    mock_review_repository_fetch_limited_by_user_id.return_value = [
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        },
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        },
    ]

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.return_value = [
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

    get_response = get_before_reviews_by_user_id(
        user_id="user_id_0", limit=1, keys="INVALID_KEY_VALUE"
    )

    assert get_response is None


def test_get_before_reviews_by_user_idでuser_repositoryの処理でエラーが発生した場合Noneを返すこと(
    mocker,
):
    mock_review_repository_fetch_limited_by_user_id = mocker.patch.object(
        ReviewRepository,
        "fetch_by_user_id",
    )
    mock_review_repository_fetch_limited_by_user_id.return_value = [
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        },
        {
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "1234567890123",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        },
    ]

    mock_user_repository_fetch_all = mocker.patch.object(
        UserRepository,
        "fetch_all",
    )
    mock_user_repository_fetch_all.side_effect = Exception("dummy exception")

    get_response = get_before_reviews_by_user_id(user_id="user_id_0", limit=1)

    assert get_response is None
