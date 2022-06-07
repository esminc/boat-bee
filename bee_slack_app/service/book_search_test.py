# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name
# pylint: disable=invalid-name
# pylint: disable=no-self-use

from bee_slack_app.repository.google_books_repository import GoogleBooksRepository
from bee_slack_app.service import book_search


class Test_search_book_by_title:
    def setup_method(self, _):
        self.book_search = book_search

    def teardown_method(self, _):
        pass

    def test_タイトル指定でヒットした場合は結果が1件以上返ってくること(self, monkeypatch):
        def mock_search_book_by_title(_, title):
            book = [
                {
                    "title": title,
                    "isbn": "1234567890123",
                    "authors": "テストの著者名_1",
                    "google_books_url": "http://books.google.co.jp/for_google_books_url_test_1",
                    "image_url": "http://books.google.co.jp/for_image_url_test_1",
                    "description": "test_description_1",
                },
                {
                    "title": "テストのタイトル_2",
                    "isbn": "1234567890123",
                    "authors": "テストの著者名_2",
                    "google_books_url": "http://books.google.co.jp/for_google_books_url_test_2",
                    "image_url": "http://books.google.co.jp/for_image_url_test_2",
                    "description": "test_description_2",
                },
                {
                    "title": "テストのタイトル_3",
                    "isbn": "1234567890123",
                    "authors": "テストの著者名_3",
                    "google_books_url": "http://books.google.co.jp/for_google_books_url_test_3",
                    "image_url": "http://books.google.co.jp/for_image_url_test_3",
                    "description": "test_description_3",
                },
            ]
            return book

        monkeypatch.setattr(
            GoogleBooksRepository, "search_book_by_title", mock_search_book_by_title
        )

        target_title = "テストのタイトル_1"

        result = self.book_search.search_book_by_title(target_title)

        assert len(result) > 0

        # 何件見つかるかは不定なので、とりあえず先頭の要素だけチェックする
        target_book = result[0]

        # 必要な要素が返ってきていること、内容の妥当性は問わない（Repository側で担保する）
        assert target_book["title"] is not None
        assert target_book["isbn"] is not None
        assert target_book["authors"] is not None
        assert target_book["google_books_url"] is not None
        assert target_book["image_url"] is not None
        assert target_book["description"] is not None

    def test_検索ワードにヒットしない場合0件の結果が返ってくること(self, monkeypatch):
        def mock_search_book_by_title(_, __):
            book = []
            return book

        monkeypatch.setattr(
            GoogleBooksRepository, "search_book_by_title", mock_search_book_by_title
        )

        target_title = "絶対にヒットしない検索ワード"

        result = self.book_search.search_book_by_title(target_title)

        assert len(result) == 0


class Test_search_book_by_isbn:
    def setup_method(self, _):
        self.book_search = book_search

    def teardown_method(self, _):
        pass

    def test_ISBN指定でヒットした場合は結果が1件であること(self, monkeypatch):
        def mock_search_book_by_isbn(_, isbn):
            book = {
                "title": "テストのタイトル",
                "isbn": isbn,
                "authors": "テストの著者名",
                "google_books_url": "http://books.google.co.jp/for_google_books_url_test",
                "image_url": "http://books.google.co.jp/for_image_url_test",
                "description": "test_description",
            }
            return book

        monkeypatch.setattr(
            GoogleBooksRepository, "search_book_by_isbn", mock_search_book_by_isbn
        )

        target_isbn = "9784873118253"

        result = self.book_search.search_book_by_isbn(target_isbn)

        assert result is not None

        # 必要な要素が返ってきていること、内容の妥当性は問わない（Repository側で担保する）
        assert result["title"] is not None
        assert result["isbn"] is not None
        assert result["authors"] is not None
        assert result["google_books_url"] is not None
        assert result["image_url"] is not None
        assert result["description"] is not None

    def test_ISBN指定でヒットしなかった場合は結果が0件であること(self, monkeypatch):
        def mock_search_book_by_isbn(_, __):
            return None

        monkeypatch.setattr(
            GoogleBooksRepository, "search_book_by_isbn", mock_search_book_by_isbn
        )

        target_isbn = "1234567890123"

        result = self.book_search.search_book_by_isbn(target_isbn)

        assert result is None
