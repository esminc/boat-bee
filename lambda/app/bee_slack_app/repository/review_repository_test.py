# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name
# pylint: disable=invalid-name
# pylint: disable=too-many-lines


import boto3  # type: ignore
from moto import mock_dynamodb  # type: ignore

from bee_slack_app.repository.database import create_table
from bee_slack_app.repository.review_repository import ReviewRepository


@mock_dynamodb
class TestReviewRepository:
    def setup_method(self, _):
        self.table = create_table()

    def test_ISBNからレビューを取得できること(self):
        item = {
            "PK": "review#user_id_0#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_0",
            "GSI_2_SK": "12345",
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "12345",
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_2#67890",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_2",
            "GSI_2_SK": "67890",
            "user_id": "user_id_2",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "2",
            "score_for_others": "4",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_2",
            "book_author": "dummy_book_author_2",
            "book_url": "dummy_book_url_2",
        }

        self.table.put_item(Item=item)

        review_repository = ReviewRepository()

        reviews = review_repository.get_by_isbn(isbn="12345")

        assert len(reviews) == 2

        assert reviews[0]["user_id"] == "user_id_0"
        assert reviews[0]["isbn"] == "12345"
        assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[0]["score_for_me"] == "1"
        assert reviews[0]["score_for_others"] == "5"
        assert reviews[0]["review_comment"] == "とても良いです"
        assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
        assert reviews[0]["book_author"] == "dummy_book_author_0"
        assert reviews[0]["book_url"] == "dummy_book_url_0"

        assert reviews[1]["user_id"] == "user_id_1"
        assert reviews[1]["isbn"] == "12345"
        assert reviews[1]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[1]["score_for_me"] == "3"
        assert reviews[1]["score_for_others"] == "4"
        assert reviews[1]["review_comment"] == "まあまあです"
        assert reviews[1]["book_image_url"] == "dummy_book_image_url_0"
        assert reviews[1]["book_author"] == "dummy_book_author_0"
        assert reviews[1]["book_url"] == "dummy_book_url_0"

    def test_テーブルに存在しないレビューのISBNを指定した場合_空配列を返すこと(self):
        item = {
            "PK": "review#user_id_0#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_0",
            "GSI_2_SK": "12345",
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "12345",
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_2#67890",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_2",
            "GSI_2_SK": "67890",
            "user_id": "user_id_2",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "2",
            "score_for_others": "4",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_2",
            "book_author": "dummy_book_author_2",
            "book_url": "dummy_book_url_2",
        }

        self.table.put_item(Item=item)

        review_repository = ReviewRepository()

        reviews = review_repository.get_by_isbn(isbn="isbn_not_exist")

        assert len(reviews) == 0
        assert isinstance(reviews, list)

    def test_ユーザIDからレビューを取得できること(self):
        item = {
            "PK": "review#user_id_0#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_0",
            "GSI_2_SK": "12345",
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "12345",
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#67890",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "67890",
            "user_id": "user_id_1",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "2",
            "score_for_others": "4",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_2",
            "book_author": "dummy_book_author_2",
            "book_url": "dummy_book_url_2",
        }

        self.table.put_item(Item=item)

        review_repository = ReviewRepository()

        reviews = review_repository.get_by_user_id(user_id="user_id_1")

        assert len(reviews) == 2

        assert reviews[0]["user_id"] == "user_id_1"
        assert reviews[0]["isbn"] == "12345"
        assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[0]["score_for_me"] == "3"
        assert reviews[0]["score_for_others"] == "4"
        assert reviews[0]["review_comment"] == "まあまあです"
        assert reviews[0]["updated_at"] == "2022-04-01T00:00:00+09:00"
        assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
        assert reviews[0]["book_author"] == "dummy_book_author_0"
        assert reviews[0]["book_url"] == "dummy_book_url_0"

        assert reviews[1]["user_id"] == "user_id_1"
        assert reviews[1]["isbn"] == "67890"
        assert reviews[1]["book_title"] == "Python チュートリアル"
        assert reviews[1]["score_for_me"] == "2"
        assert reviews[1]["score_for_others"] == "4"
        assert reviews[1]["review_comment"] == "そこそこです"
        assert reviews[1]["updated_at"] == "2022-04-02T00:00:00+09:00"
        assert reviews[1]["book_image_url"] == "dummy_book_image_url_2"
        assert reviews[1]["book_author"] == "dummy_book_author_2"
        assert reviews[1]["book_url"] == "dummy_book_url_2"

    def test_個数を指定してユーザIDからレビューを取得できること(self):
        item = {
            "PK": "review#user_id_0#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_0",
            "GSI_2_SK": "12345",
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "12345",
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#67890",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "67890",
            "user_id": "user_id_1",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "2",
            "score_for_others": "4",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_2",
            "book_author": "dummy_book_author_2",
            "book_url": "dummy_book_url_2",
        }

        self.table.put_item(Item=item)

        review_repository = ReviewRepository()

        get_response = review_repository.get_limited_by_user_id(
            user_id="user_id_1", limit=1
        )

        reviews = get_response["items"]

        assert len(reviews) == 1

        assert reviews[0]["user_id"] == "user_id_1"
        assert reviews[0]["isbn"] == "12345"
        assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[0]["score_for_me"] == "3"
        assert reviews[0]["score_for_others"] == "4"
        assert reviews[0]["review_comment"] == "まあまあです"
        assert reviews[0]["updated_at"] == "2022-04-01T00:00:00+09:00"
        assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
        assert reviews[0]["book_author"] == "dummy_book_author_0"
        assert reviews[0]["book_url"] == "dummy_book_url_0"

    def test_KEYを指定して続きのレビューを取得できること(self):
        item = {
            "PK": "review#user_id_0#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_0",
            "GSI_2_SK": "12345",
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "12345",
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#67890",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "67890",
            "user_id": "user_id_1",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "2",
            "score_for_others": "4",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_2",
            "book_author": "dummy_book_author_2",
            "book_url": "dummy_book_url_2",
        }

        self.table.put_item(Item=item)

        review_repository = ReviewRepository()

        get_response = review_repository.get_limited_by_user_id(
            user_id="user_id_1", limit=1
        )

        key = get_response["last_key"]

        get_response = review_repository.get_limited_by_user_id(
            user_id="user_id_1", limit=1, start_key=key
        )

        reviews = get_response["items"]

        assert len(reviews) == 1

        assert reviews[0]["user_id"] == "user_id_1"
        assert reviews[0]["isbn"] == "67890"
        assert reviews[0]["book_title"] == "Python チュートリアル"
        assert reviews[0]["score_for_me"] == "2"
        assert reviews[0]["score_for_others"] == "4"
        assert reviews[0]["review_comment"] == "そこそこです"
        assert reviews[0]["updated_at"] == "2022-04-02T00:00:00+09:00"
        assert reviews[0]["book_image_url"] == "dummy_book_image_url_2"
        assert reviews[0]["book_author"] == "dummy_book_author_2"
        assert reviews[0]["book_url"] == "dummy_book_url_2"

    def test_存在する以上の個数を指定した場合は存在する分のレビューを取得できること(self):
        item = {
            "PK": "review#user_id_0#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_0",
            "GSI_2_SK": "12345",
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "12345",
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#67890",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "67890",
            "user_id": "user_id_1",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "2",
            "score_for_others": "4",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_2",
            "book_author": "dummy_book_author_2",
            "book_url": "dummy_book_url_2",
        }

        self.table.put_item(Item=item)

        review_repository = ReviewRepository()

        get_response = review_repository.get_limited_by_user_id(
            user_id="user_id_1", limit=5
        )

        reviews = get_response["items"]

        assert len(reviews) == 2

        assert reviews[0]["user_id"] == "user_id_1"
        assert reviews[0]["isbn"] == "12345"
        assert reviews[0]["book_title"] == "仕事ではじめる機械学習"
        assert reviews[0]["score_for_me"] == "3"
        assert reviews[0]["score_for_others"] == "4"
        assert reviews[0]["review_comment"] == "まあまあです"
        assert reviews[0]["updated_at"] == "2022-04-01T00:00:00+09:00"
        assert reviews[0]["book_image_url"] == "dummy_book_image_url_0"
        assert reviews[0]["book_author"] == "dummy_book_author_0"
        assert reviews[0]["book_url"] == "dummy_book_url_0"

        assert reviews[1]["user_id"] == "user_id_1"
        assert reviews[1]["isbn"] == "67890"
        assert reviews[1]["book_title"] == "Python チュートリアル"
        assert reviews[1]["score_for_me"] == "2"
        assert reviews[1]["score_for_others"] == "4"
        assert reviews[1]["review_comment"] == "そこそこです"
        assert reviews[1]["updated_at"] == "2022-04-02T00:00:00+09:00"
        assert reviews[1]["book_image_url"] == "dummy_book_image_url_2"
        assert reviews[1]["book_author"] == "dummy_book_author_2"
        assert reviews[1]["book_url"] == "dummy_book_url_2"

    def test_個数と存在しないユーザIDを指定した場合_空配列を返すこと(self):
        item = {
            "PK": "review#user_id_0#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_0",
            "GSI_2_SK": "12345",
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "12345",
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#67890",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "67890",
            "user_id": "user_id_1",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "2",
            "score_for_others": "4",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_2",
            "book_author": "dummy_book_author_2",
            "book_url": "dummy_book_url_2",
        }

        self.table.put_item(Item=item)

        review_repository = ReviewRepository()

        get_response = review_repository.get_limited_by_user_id(
            user_id="non_user_id", limit=1
        )

        reviews = get_response["items"]

        assert len(reviews) == 0

    def test_テーブルに存在しないレビューのユーザIDを指定した場合_空配列を返すこと(self):
        item = {
            "PK": "review#user_id_0#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_0",
            "GSI_2_SK": "12345",
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "12345",
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_2#67890",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_2",
            "GSI_2_SK": "67890",
            "user_id": "user_id_2",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "2",
            "score_for_others": "4",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_2",
            "book_author": "dummy_book_author_2",
            "book_url": "dummy_book_url_2",
        }

        self.table.put_item(Item=item)

        review_repository = ReviewRepository()

        reviews = review_repository.get_by_user_id(user_id="user_id_not_exist")

        assert len(reviews) == 0
        assert isinstance(reviews, list)

    def test_レビューを一意に指定して取得できること(self):
        item = {
            "PK": "review#user_id_0#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_0",
            "GSI_2_SK": "12345",
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "12345",
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_2#67890",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_2",
            "GSI_2_SK": "67890",
            "user_id": "user_id_2",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "2",
            "score_for_others": "4",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_2",
            "book_author": "dummy_book_author_2",
            "book_url": "dummy_book_url_2",
            "book_description": "dummy_description_2",
        }

        self.table.put_item(Item=item)

        review_repository = ReviewRepository()

        review = review_repository.get(user_id="user_id_1", isbn="12345")

        assert review["user_id"] == "user_id_1"
        assert review["isbn"] == "12345"
        assert review["book_title"] == "仕事ではじめる機械学習"
        assert review["score_for_me"] == "3"
        assert review["score_for_others"] == "4"
        assert review["review_comment"] == "まあまあです"
        assert review["book_image_url"] == "dummy_book_image_url_1"
        assert review["book_author"] == "dummy_book_author_1"
        assert review["book_url"] == "dummy_book_url_1"
        assert review["book_description"] == "dummy_description_1"

    def test_存在しないレビューを指定した場合_Noneを返すこと(self):
        item = {
            "PK": "review#user_id_0#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_0",
            "GSI_2_SK": "12345",
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "12345",
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_2#67890",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_2",
            "GSI_2_SK": "67890",
            "user_id": "user_id_2",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "2",
            "score_for_others": "4",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_2",
            "book_author": "dummy_book_author_2",
            "book_url": "dummy_book_url_2",
            "book_description": "dummy_description_2",
        }

        self.table.put_item(Item=item)

        review_repository = ReviewRepository()

        review = review_repository.get(user_id="user_id_not_exist", isbn="12345")

        assert review is None

    def test_全件取得でレビューを取得できること(self):
        item = {
            "PK": "review#user_id_0#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_0",
            "GSI_2_SK": "12345",
            "user_id": "user_id_0",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "1",
            "score_for_others": "5",
            "review_comment": "とても良いです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_0",
            "book_author": "dummy_book_author_0",
            "book_url": "dummy_book_url_0",
            "book_description": "dummy_description_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_1#12345",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-01T00:00:00+09:00",
            "GSI_1_SK": "user_id_1",
            "GSI_2_SK": "12345",
            "user_id": "user_id_1",
            "book_title": "仕事ではじめる機械学習",
            "isbn": "12345",
            "score_for_me": "3",
            "score_for_others": "4",
            "review_comment": "まあまあです",
            "updated_at": "2022-04-01T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_1",
            "book_author": "dummy_book_author_1",
            "book_url": "dummy_book_url_1",
            "book_description": "dummy_description_1",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "review#user_id_2#67890",
            "GSI_PK": "review",
            "GSI_0_SK": "2022-04-02T00:00:00+09:00",
            "GSI_1_SK": "user_id_2",
            "GSI_2_SK": "67890",
            "user_id": "user_id_2",
            "book_title": "Python チュートリアル",
            "isbn": "67890",
            "score_for_me": "2",
            "score_for_others": "4",
            "review_comment": "そこそこです",
            "updated_at": "2022-04-02T00:00:00+09:00",
            "book_image_url": "dummy_book_image_url_2",
            "book_author": "dummy_book_author_2",
            "book_url": "dummy_book_url_2",
            "book_description": "dummy_description_2",
        }

        self.table.put_item(Item=item)

        review_repository = ReviewRepository()

        reviews = review_repository.get_all()

        assert len(reviews) == 3

        assert reviews[0]["user_id"] == "user_id_0"
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
        assert reviews[2]["isbn"] == "67890"
        assert reviews[2]["book_title"] == "Python チュートリアル"
        assert reviews[2]["score_for_me"] == "2"
        assert reviews[2]["score_for_others"] == "4"
        assert reviews[2]["review_comment"] == "そこそこです"
        assert reviews[2]["book_image_url"] == "dummy_book_image_url_2"
        assert reviews[2]["book_author"] == "dummy_book_author_2"
        assert reviews[2]["book_url"] == "dummy_book_url_2"
        assert reviews[2]["book_description"] == "dummy_description_2"

    def test_全件取得でレビューが0件の場合_空配列を返すこと(self):
        response = self.table.scan()

        assert len(response["Items"]) == 0

        review_repository = ReviewRepository()

        reviews = review_repository.get_all()

        assert len(reviews) == 0
        assert isinstance(reviews, list)

    def test_レビューを作成できること(self):
        item = self.table.get_item(Key={"PK": "review#test_user_id#12345"}).get("Item")

        assert item is None

        review_repository = ReviewRepository()

        review_repository.create(
            {
                "user_id": "test_user_id",
                "isbn": "12345",
                "book_title": "本のタイトル",
                "score_for_me": "1",
                "score_for_others": "3",
                "review_comment": "レビューコメント",
                "updated_at": "2022-04-01T00:00:00+09:00",
                "book_image_url": "dummy_book_image_url",
                "book_author": "dummy_book_author",
                "book_url": "dummy_book_url",
                "book_description": "dummy_description",
            }
        )

        actual = self.table.get_item(Key={"PK": "review#test_user_id#12345"}).get(
            "Item"
        )
        assert actual["PK"] == "review#test_user_id#12345"
        assert actual["GSI_PK"] == "review"
        assert actual["GSI_0_SK"] == "2022-04-01T00:00:00+09:00"
        assert actual["GSI_1_SK"] == "test_user_id"
        assert actual["GSI_2_SK"] == "12345"
        assert actual["user_id"] == "test_user_id"
        assert actual["isbn"] == "12345"
        assert actual["book_title"] == "本のタイトル"
        assert actual["score_for_me"] == "1"
        assert actual["score_for_others"] == "3"
        assert actual["review_comment"] == "レビューコメント"
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"
        assert actual["book_image_url"] == "dummy_book_image_url"
        assert actual["book_author"] == "dummy_book_author"
        assert actual["book_url"] == "dummy_book_url"
        assert actual["book_description"] == "dummy_description"

    def test_レビューを上書きできること(self):
        review_repository = ReviewRepository()

        review_repository.create(
            {
                "user_id": "test_user_id",
                "isbn": "12345",
                "book_title": "最初のレビューのタイトル",
                "score_for_me": "1",
                "score_for_others": "3",
                "review_comment": "最初のレビューのコメント",
                "updated_at": "2022-04-01T00:00:00+09:00",
                "book_image_url": "dummy_book_image_url",
                "book_author": "dummy_book_author",
                "book_url": "dummy_book_url",
                "book_description": "dummy_description",
            }
        )

        actual = self.table.get_item(Key={"PK": "review#test_user_id#12345"}).get(
            "Item"
        )

        assert actual["PK"] == "review#test_user_id#12345"
        assert actual["GSI_PK"] == "review"
        assert actual["GSI_0_SK"] == "2022-04-01T00:00:00+09:00"
        assert actual["GSI_1_SK"] == "test_user_id"
        assert actual["GSI_2_SK"] == "12345"
        assert actual["user_id"] == "test_user_id"
        assert actual["isbn"] == "12345"
        assert actual["book_title"] == "最初のレビューのタイトル"
        assert actual["score_for_me"] == "1"
        assert actual["score_for_others"] == "3"
        assert actual["review_comment"] == "最初のレビューのコメント"
        assert actual["updated_at"] == "2022-04-01T00:00:00+09:00"
        assert actual["book_image_url"] == "dummy_book_image_url"
        assert actual["book_author"] == "dummy_book_author"
        assert actual["book_url"] == "dummy_book_url"
        assert actual["book_description"] == "dummy_description"

        review_repository.create(
            {
                "user_id": "test_user_id",
                "isbn": "12345",
                "book_title": "上書き後のレビューのタイトル",
                "score_for_me": "1",
                "score_for_others": "3",
                "review_comment": "上書き後のレビューのコメント",
                "updated_at": "2022-04-02T00:00:00+09:00",
                "book_image_url": "dummy_book_image_url",
                "book_author": "dummy_book_author",
                "book_url": "dummy_book_url",
                "book_description": "dummy_description",
            }
        )

        actual = self.table.get_item(Key={"PK": "review#test_user_id#12345"}).get(
            "Item"
        )

        assert actual["PK"] == "review#test_user_id#12345"
        assert actual["GSI_PK"] == "review"
        assert actual["GSI_0_SK"] == "2022-04-02T00:00:00+09:00"
        assert actual["GSI_1_SK"] == "test_user_id"
        assert actual["GSI_2_SK"] == "12345"
        assert actual["user_id"] == "test_user_id"
        assert actual["isbn"] == "12345"
        assert actual["book_title"] == "上書き後のレビューのタイトル"
        assert actual["score_for_me"] == "1"
        assert actual["score_for_others"] == "3"
        assert actual["review_comment"] == "上書き後のレビューのコメント"
        assert actual["updated_at"] == "2022-04-02T00:00:00+09:00"
        assert actual["book_image_url"] == "dummy_book_image_url"
        assert actual["book_author"] == "dummy_book_author"
        assert actual["book_url"] == "dummy_book_url"
        assert actual["book_description"] == "dummy_description"

    def test_同じuser_idで別々のisbnの場合_別々のアイテムとして登録すること(self):
        response = self.table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("user_id").eq(
                "test_user_id"
            ),
        )

        assert len(response["Items"]) == 0

        review_repository = ReviewRepository()

        review_repository.create(
            {
                "user_id": "test_user_id",
                "isbn": "12345",
                "book_title": "本のタイトル",
                "score_for_me": "1",
                "score_for_others": "3",
                "review_comment": "レビューコメント",
                "updated_at": "2022-04-01T00:00:00+09:00",
                "book_image_url": "dummy_book_image_url_0",
                "book_author": "dummy_book_author_0",
                "book_url": "dummy_book_url_0",
                "book_description": "dummy_description_0",
            }
        )

        review_repository.create(
            {
                "user_id": "test_user_id",
                "isbn": "67890",
                "book_title": "本のタイトル",
                "score_for_me": "1",
                "score_for_others": "3",
                "review_comment": "レビューコメント",
                "updated_at": "2022-05-01T00:00:00+09:00",
                "book_image_url": "dummy_book_image_url_1",
                "book_author": "dummy_book_author_1",
                "book_url": "dummy_book_url_1",
                "book_description": "dummy_description_1",
            }
        )

        actual_0 = self.table.get_item(Key={"PK": "review#test_user_id#12345"}).get(
            "Item"
        )

        assert actual_0["PK"] == "review#test_user_id#12345"
        assert actual_0["GSI_PK"] == "review"
        assert actual_0["GSI_0_SK"] == "2022-04-01T00:00:00+09:00"
        assert actual_0["GSI_1_SK"] == "test_user_id"
        assert actual_0["GSI_2_SK"] == "12345"
        assert actual_0["user_id"] == "test_user_id"
        assert actual_0["isbn"] == "12345"
        assert actual_0["book_title"] == "本のタイトル"
        assert actual_0["score_for_me"] == "1"
        assert actual_0["score_for_others"] == "3"
        assert actual_0["review_comment"] == "レビューコメント"
        assert actual_0["updated_at"] == "2022-04-01T00:00:00+09:00"
        assert actual_0["book_image_url"] == "dummy_book_image_url_0"
        assert actual_0["book_author"] == "dummy_book_author_0"
        assert actual_0["book_url"] == "dummy_book_url_0"
        assert actual_0["book_description"] == "dummy_description_0"

        actual_1 = self.table.get_item(Key={"PK": "review#test_user_id#67890"}).get(
            "Item"
        )

        assert actual_1["PK"] == "review#test_user_id#67890"
        assert actual_1["GSI_PK"] == "review"
        assert actual_1["GSI_0_SK"] == "2022-05-01T00:00:00+09:00"
        assert actual_1["GSI_1_SK"] == "test_user_id"
        assert actual_1["GSI_2_SK"] == "67890"
        assert actual_1["user_id"] == "test_user_id"
        assert actual_1["isbn"] == "67890"
        assert actual_1["book_title"] == "本のタイトル"
        assert actual_1["score_for_me"] == "1"
        assert actual_1["score_for_others"] == "3"
        assert actual_1["review_comment"] == "レビューコメント"
        assert actual_1["updated_at"] == "2022-05-01T00:00:00+09:00"
        assert actual_1["book_image_url"] == "dummy_book_image_url_1"
        assert actual_1["book_author"] == "dummy_book_author_1"
        assert actual_1["book_url"] == "dummy_book_url_1"
        assert actual_1["book_description"] == "dummy_description_1"
