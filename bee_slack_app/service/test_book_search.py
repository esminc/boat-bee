# pylint: disable=attribute-defined-outside-init
# pylint: disable=duplicate-code
# pylint: disable=non-ascii-name

from bee_slack_app.service import book_search
from bee_slack_app.repository.google_books import GoogleBooks

# TODO:
# このテストケースは外部に依存しているため本来の意味では
# ユニットテストとして不適切（期待値を確定できないため）
# 今回は外部APIの利用方法を確認する目的を兼ねてここでテストを行う
# ここに記載した期待値は現時点では正しく得られるが、Google Books API側の
# 変更などによりこちらのコードに手を加えなくてもFAILするリスクがあることに注意


class TestBookSearch:
    def setup_method(self, _):
        self.book_search = book_search

    def teardown_method(self, _):
        pass

    def test_正確にタイトルを指定して検索結果が得られること(self, monkeypatch):
        def mock_search_book_by_title(_, title):
            book = [
                {
                    "title": title,
                    "isbn": "1234567890123",
                    "author": "テストの著者名_1",
                    "google_books_url": "http://books.google.co.jp/for_google_books_url_test_1",
                    "image_url": "http://books.google.co.jp/for_image_url_test_1",
                },
                {
                    "title": "テストのタイトル_2",
                    "isbn": "1234567890123",
                    "author": "テストの著者名_2",
                    "google_books_url": "http://books.google.co.jp/for_google_books_url_test_2",
                    "image_url": "http://books.google.co.jp/for_image_url_test_2",
                },
                {
                    "title": "テストのタイトル_3",
                    "isbn": "1234567890123",
                    "author": "テストの著者名_3",
                    "google_books_url": "http://books.google.co.jp/for_google_books_url_test_3",
                    "image_url": "http://books.google.co.jp/for_image_url_test_3",
                },
            ]
            return book

        monkeypatch.setattr(
            GoogleBooks, "search_book_by_title", mock_search_book_by_title
        )

        target_title = "テストのタイトル_1"

        result = self.book_search.search_book_by_title(target_title)

        assert len(result) > 0

        target_books = [x for x in result if x["title"] == target_title]
        assert len(target_books) == 1

        target_book = target_books[0]
        assert target_book["isbn"] == "1234567890123"
        assert target_book["author"] is not None

        assert (
            target_book["google_books_url"]
            == "http://books.google.co.jp/for_google_books_url_test_1"
        )
        assert (
            target_book["image_url"] == "http://books.google.co.jp/for_image_url_test_1"
        )

    def test_曖昧にタイトルを指定して検索結果が得られること(self, monkeypatch):
        def mock_search_book_by_title(_, __):
            book = [
                {
                    "title": "テストのタイトル_1",
                    "isbn": "1234567890123",
                    "author": "テストの著者名_1",
                    "google_books_url": "http://books.google.co.jp/for_google_books_url_test_1",
                    "image_url": "http://books.google.co.jp/for_image_url_test_1",
                },
                {
                    "title": "テストのタイトル_2",
                    "isbn": "1234567890123",
                    "author": "テストの著者名_2",
                    "google_books_url": "http://books.google.co.jp/for_google_books_url_test_2",
                    "image_url": "http://books.google.co.jp/for_image_url_test_2",
                },
                {
                    "title": "テストのタイトル_3",
                    "isbn": "1234567890123",
                    "author": "テストの著者名_3",
                    "google_books_url": "http://books.google.co.jp/for_google_books_url_test_3",
                    "image_url": "http://books.google.co.jp/for_image_url_test_3",
                },
            ]
            return book

        monkeypatch.setattr(
            GoogleBooks, "search_book_by_title", mock_search_book_by_title
        )

        target_title = "曖昧な検索ワード"

        result = self.book_search.search_book_by_title(target_title)

        assert len(result) > 0

    def test_曖昧に複数の単語を指定して検索結果が得られること(self, monkeypatch):
        def mock_search_book_by_title(_, __):
            book = [
                {
                    "title": "テストのタイトル_1",
                    "isbn": "1234567890123",
                    "author": "テストの著者名_1",
                    "google_books_url": "http://books.google.co.jp/for_google_books_url_test_1",
                    "image_url": "http://books.google.co.jp/for_image_url_test_1",
                },
                {
                    "title": "テストのタイトル_2",
                    "isbn": "1234567890123",
                    "author": "テストの著者名_2",
                    "google_books_url": "http://books.google.co.jp/for_google_books_url_test_2",
                    "image_url": "http://books.google.co.jp/for_image_url_test_2",
                },
                {
                    "title": "テストのタイトル_3",
                    "isbn": "1234567890123",
                    "author": "テストの著者名_3",
                    "google_books_url": "http://books.google.co.jp/for_google_books_url_test_3",
                    "image_url": "http://books.google.co.jp/for_image_url_test_3",
                },
            ]
            return book

        monkeypatch.setattr(
            GoogleBooks, "search_book_by_title", mock_search_book_by_title
        )

        target_title = "仕事ではじめる 適当な 検索ワード"

        result = self.book_search.search_book_by_title(target_title)

        assert len(result) > 0

    def test_検索ワードにヒットしない場合0件の結果が返ってくること(self, monkeypatch):
        def mock_search_book_by_title(_, __):
            book = []
            return book

        monkeypatch.setattr(
            GoogleBooks, "search_book_by_title", mock_search_book_by_title
        )

        target_title = "絶対にヒットしない検索ワード"

        result = self.book_search.search_book_by_title(target_title)

        assert len(result) == 0

    def test_13桁の正当なISBNを指定したら結果が1件だけ得られること(
        self, monkeypatch
    ):  # pylint: disable=invalid-name
        def mock_search_book_by_isbn(_, isbn):
            book = {
                "title": "テストのタイトル",
                "isbn": isbn,
                "author": "テストの著者名",
                "google_books_url": "http://books.google.co.jp/for_google_books_url_test",
                "image_url": "http://books.google.co.jp/for_image_url_test",
            }
            return book

        monkeypatch.setattr(
            GoogleBooks, "search_book_by_isbn", mock_search_book_by_isbn
        )

        target_isbn = "9784873118253"

        result = self.book_search.search_book_by_isbn(target_isbn)

        assert result is not None
        assert result["title"] == "テストのタイトル"
        assert result["isbn"] == target_isbn
        assert result["author"] == "テストの著者名"

        assert (
            result["google_books_url"]
            == "http://books.google.co.jp/for_google_books_url_test"
        )
        assert result["image_url"] == "http://books.google.co.jp/for_image_url_test"

    def test_10桁の正当なISBNを指定したら結果が1件だけ得られること(
        self, monkeypatch
    ):  # pylint: disable=invalid-name
        def mock_search_book_by_isbn(_, isbn):
            book = {
                "title": "テストのタイトル",
                "isbn": isbn,
                "author": "テストの著者名",
                "google_books_url": "http://books.google.co.jp/for_google_books_url_test",
                "image_url": "http://books.google.co.jp/for_image_url_test",
            }
            return book

        monkeypatch.setattr(
            GoogleBooks, "search_book_by_isbn", mock_search_book_by_isbn
        )

        target_isbn = "4873118255"

        result = self.book_search.search_book_by_isbn(target_isbn)

        assert result is not None
        assert result["title"] == "テストのタイトル"
        assert result["isbn"] == target_isbn
        assert result["author"] == "テストの著者名"

        assert (
            result["google_books_url"]
            == "http://books.google.co.jp/for_google_books_url_test"
        )
        assert result["image_url"] == "http://books.google.co.jp/for_image_url_test"

    def test_存在しないISBNを指定したら結果が0件であること(
        self, monkeypatch
    ):  # pylint: disable=invalid-name
        def mock_search_book_by_isbn(_, __):
            return None

        monkeypatch.setattr(
            GoogleBooks, "search_book_by_isbn", mock_search_book_by_isbn
        )

        target_isbn = "1234567890123"

        result = self.book_search.search_book_by_isbn(target_isbn)

        assert result is None

    def test_13桁ではない不正なISBNを指定したら結果が0件であること(
        self, monkeypatch
    ):  # pylint: disable=invalid-name
        def mock_search_book_by_isbn(_, __):
            return None

        monkeypatch.setattr(
            GoogleBooks, "search_book_by_isbn", mock_search_book_by_isbn
        )

        target_isbn = "123"

        result = self.book_search.search_book_by_isbn(target_isbn)

        assert result is None
