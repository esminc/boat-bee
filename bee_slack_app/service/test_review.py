# pylint: disable=non-ascii-name


from injector import Injector, inject

from bee_slack_app.repository.book_repository import BookRepository
from bee_slack_app.repository.review_repository import ReviewRepository
from bee_slack_app.repository.user_repository import UserRepository
from bee_slack_app.service.review import ReviewService
from bee_slack_app.utils import datetime


def test_get_reviewでレビューを取得できること(mocker):
    def configure_for_testing(binder):
        review_repository = mocker.Mock()
        attrs = {
            "get.return_value": {
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
        }
        review_repository.configure_mock(**attrs)
        binder.bind(ReviewRepository, to=review_repository)

    def configure_user_repository(binder):
        mock = mocker.Mock()
        attrs = {
            "get.return_value": {
                "user_id": "user_id_0",
                "department": "department_0",
                "job_type": "job_type_0",
                "age_range": "age_range_0",
                "updated_at": "2022-04-11T09:23:04+09:00",
                "user_name": "user_name_0",
            }
        }
        mock.configure_mock(**attrs)
        binder.bind(UserRepository, to=mock)

    injector = Injector([configure_for_testing, configure_user_repository])

    review_service = injector.get(ReviewService)

    review = review_service.get_review(user_id="user_id_0", isbn="12345")

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
