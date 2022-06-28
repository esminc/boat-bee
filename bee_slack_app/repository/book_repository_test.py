# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name
# pylint: disable=invalid-name

from moto import mock_dynamodb  # type: ignore

from bee_slack_app.model import Book
from bee_slack_app.repository.book_repository import BookRepository
from bee_slack_app.repository.database import create_table


@mock_dynamodb
class TestBookRepository:
    def setup_method(self, _):
        self.table = create_table()

    def test_本を保存できること(self):

        book_repository = BookRepository()

        item: Book = {
            "isbn": "12345",
            "title": "dummy_title",
            "author": "dummy_author",
            "url": "dummy_url",
            "image_url": "dummy_image_url",
            "description": "dummy_description",
            "updated_at": "2022-04-01T00:00:00+09:00",
        }

        book_repository.put(book=item)

        response = self.table.get_item(Key={"PK": "book#12345"})

        books_item = response["Item"]

        assert books_item["PK"] == "book#12345"
        assert books_item["GSI_PK"] == "book"
        assert books_item["GSI_0_SK"] == "251753562000.0"
        assert books_item["isbn"] == "12345"
        assert books_item["updated_at"] == "251753562000.0"
        assert books_item["title"] == "dummy_title"
        assert books_item["author"] == "dummy_author"
        assert books_item["url"] == "dummy_url"
        assert books_item["image_url"] == "dummy_image_url"
        assert books_item["description"] == "dummy_description"

    def test_本を取得できること(self):
        item = {
            "PK": "book#12345",
            "GSI_PK": "book",
            "GSI_0_SK": "251753562000.0",
            "isbn": "12345",
            "updated_at": "251753562000.0",
            "title": "dummy_title_0",
            "author": "dummy_author_0",
            "url": "dummy_url_0",
            "image_url": "dummy_image_url_0",
            "description": "dummy_description_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "book#67890",
            "GSI_PK": "book",
            "GSI_0_SK": "251753475600.0",
            "isbn": "67890",
            "updated_at": "251753475600.0",
            "title": "dummy_title_1",
            "author": "dummy_author_1",
            "url": "dummy_url_1",
            "image_url": "dummy_image_url_1",
            "description": "dummy_description_1",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "book#01234",
            "GSI_PK": "book",
            "GSI_0_SK": "251753389200.0",
            "isbn": "01234",
            "updated_at": "251753389200.0",
            "title": "dummy_title_2",
            "author": "dummy_author_2",
            "url": "dummy_url_2",
            "image_url": "dummy_image_url_2",
            "description": "dummy_description_2",
        }

        self.table.put_item(Item=item)

        book_repository = BookRepository()

        book = book_repository.fetch(isbn="01234")

        assert book["isbn"] == "01234"
        assert book["title"] == "dummy_title_2"
        assert book["author"] == "dummy_author_2"
        assert book["url"] == "dummy_url_2"
        assert book["image_url"] == "dummy_image_url_2"
        assert book["description"] == "dummy_description_2"
        assert book["updated_at"] == "2022-04-03T00:00:00+09:00"

    def test_fetchで本が存在しない場合はNoneを返すこと(self):
        item = {
            "PK": "book#12345",
            "GSI_PK": "book",
            "GSI_0_SK": "251753562000.0",
            "isbn": "12345",
            "updated_at": "251753562000.0",
            "title": "dummy_title_0",
            "author": "dummy_author_0",
            "url": "dummy_url_0",
            "image_url": "dummy_image_url_0",
            "description": "dummy_description_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "book#67890",
            "GSI_PK": "book",
            "GSI_0_SK": "251753475600.0",
            "isbn": "67890",
            "updated_at": "251753475600.0",
            "title": "dummy_title_1",
            "author": "dummy_author_1",
            "url": "dummy_url_1",
            "image_url": "dummy_image_url_1",
            "description": "dummy_description_1",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "book#01234",
            "GSI_PK": "book",
            "GSI_0_SK": "251753389200.0",
            "isbn": "01234",
            "updated_at": "251753389200.0",
            "title": "dummy_title_2",
            "author": "dummy_author_2",
            "url": "dummy_url_2",
            "image_url": "dummy_image_url_2",
            "description": "dummy_description_2",
        }

        self.table.put_item(Item=item)

        book_repository = BookRepository()

        book = book_repository.fetch(isbn="isbn_not_exist")

        assert book is None

    def test_fetch_allで本を取得できること(self):
        item = {
            "PK": "book#12345",
            "GSI_PK": "book",
            "GSI_0_SK": "251753562000.0",
            "isbn": "12345",
            "updated_at": "251753562000.0",
            "title": "dummy_title_0",
            "author": "dummy_author_0",
            "url": "dummy_url_0",
            "image_url": "dummy_image_url_0",
            "description": "dummy_description_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "book#67890",
            "GSI_PK": "book",
            "GSI_0_SK": "251753475600.0",
            "isbn": "67890",
            "updated_at": "251753475600.0",
            "title": "dummy_title_1",
            "author": "dummy_author_1",
            "url": "dummy_url_1",
            "image_url": "dummy_image_url_1",
            "description": "dummy_description_1",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "book#01234",
            "GSI_PK": "book",
            "GSI_0_SK": "251753389200.0",
            "isbn": "01234",
            "updated_at": "251753389200.0",
            "title": "dummy_title_2",
            "author": "dummy_author_2",
            "url": "dummy_url_2",
            "image_url": "dummy_image_url_2",
            "description": "dummy_description_2",
        }

        self.table.put_item(Item=item)

        book_repository = BookRepository()

        books = book_repository.fetch_all()

        books_items = books["items"]

        assert len(books_items) == 3

        # レビュー投稿日時が新しい順にソート済み

        assert books_items[0]["isbn"] == "01234"
        assert books_items[0]["title"] == "dummy_title_2"
        assert books_items[0]["author"] == "dummy_author_2"
        assert books_items[0]["url"] == "dummy_url_2"
        assert books_items[0]["image_url"] == "dummy_image_url_2"
        assert books_items[0]["description"] == "dummy_description_2"
        assert books_items[0]["updated_at"] == "2022-04-03T00:00:00+09:00"

        assert books_items[1]["isbn"] == "67890"
        assert books_items[1]["title"] == "dummy_title_1"
        assert books_items[1]["author"] == "dummy_author_1"
        assert books_items[1]["url"] == "dummy_url_1"
        assert books_items[1]["image_url"] == "dummy_image_url_1"
        assert books_items[1]["description"] == "dummy_description_1"
        assert books_items[1]["updated_at"] == "2022-04-02T00:00:00+09:00"

        assert books_items[2]["isbn"] == "12345"
        assert books_items[2]["title"] == "dummy_title_0"
        assert books_items[2]["author"] == "dummy_author_0"
        assert books_items[2]["url"] == "dummy_url_0"
        assert books_items[2]["image_url"] == "dummy_image_url_0"
        assert books_items[2]["description"] == "dummy_description_0"
        assert books_items[2]["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_fetch_allで複数回に分けて本を取得できること(self):
        item = {
            "PK": "book#12345",
            "GSI_PK": "book",
            "GSI_0_SK": "251753562000.0",
            "isbn": "12345",
            "updated_at": "251753562000.0",
            "title": "dummy_title_0",
            "author": "dummy_author_0",
            "url": "dummy_url_0",
            "image_url": "dummy_image_url_0",
            "description": "dummy_description_0",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "book#67890",
            "GSI_PK": "book",
            "GSI_0_SK": "251753475600.0",
            "isbn": "67890",
            "updated_at": "251753475600.0",
            "title": "dummy_title_1",
            "author": "dummy_author_1",
            "url": "dummy_url_1",
            "image_url": "dummy_image_url_1",
            "description": "dummy_description_1",
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "book#01234",
            "GSI_PK": "book",
            "GSI_0_SK": "251753389200.0",
            "isbn": "01234",
            "updated_at": "251753389200.0",
            "title": "dummy_title_2",
            "author": "dummy_author_2",
            "url": "dummy_url_2",
            "image_url": "dummy_image_url_2",
            "description": "dummy_description_2",
        }

        self.table.put_item(Item=item)

        book_repository = BookRepository()

        # 1回目
        books = book_repository.fetch_all(limit=2)

        books_items = books["items"]

        assert len(books_items) == 2

        # レビュー投稿日時が新しい順にソート済み

        assert books_items[0]["isbn"] == "01234"
        assert books_items[0]["title"] == "dummy_title_2"
        assert books_items[0]["author"] == "dummy_author_2"
        assert books_items[0]["url"] == "dummy_url_2"
        assert books_items[0]["image_url"] == "dummy_image_url_2"
        assert books_items[0]["description"] == "dummy_description_2"
        assert books_items[0]["updated_at"] == "2022-04-03T00:00:00+09:00"

        assert books_items[1]["isbn"] == "67890"
        assert books_items[1]["title"] == "dummy_title_1"
        assert books_items[1]["author"] == "dummy_author_1"
        assert books_items[1]["url"] == "dummy_url_1"
        assert books_items[1]["image_url"] == "dummy_image_url_1"
        assert books_items[1]["description"] == "dummy_description_1"
        assert books_items[1]["updated_at"] == "2022-04-02T00:00:00+09:00"

        # 2回目
        books = book_repository.fetch_all(limit=2, start_key=books["last_key"])

        books_items = books["items"]

        assert len(books_items) == 1

        assert books_items[0]["isbn"] == "12345"
        assert books_items[0]["title"] == "dummy_title_0"
        assert books_items[0]["author"] == "dummy_author_0"
        assert books_items[0]["url"] == "dummy_url_0"
        assert books_items[0]["image_url"] == "dummy_image_url_0"
        assert books_items[0]["description"] == "dummy_description_0"
        assert books_items[0]["updated_at"] == "2022-04-01T00:00:00+09:00"

    def test_fetch_allで本が存在しない場合は空配列を返すこと(self):
        response = self.table.scan()

        assert len(response["Items"]) == 0

        book_repository = BookRepository()

        books = book_repository.fetch_all()

        books_items = books["items"]
        books_last_key = books["last_key"]

        assert len(books_items) == 0
        assert books_last_key is None
