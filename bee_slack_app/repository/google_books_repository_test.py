# pylint: disable=attribute-defined-outside-init

# pylint: disable=non-ascii-name

from bee_slack_app.repository.google_books_repository import GoogleBooksRepository

# TODO:
# このテストケースは外部に依存しているため本来の意味では
# ユニットテストとして不適切（期待値を確定できないため）
# 今回は外部APIの利用方法を確認する目的を兼ねてここでテストを行う
# ここに記載した期待値は現時点では正しく得られるが、Google Books API側の
# 変更などによりこちらのコードに手を加えなくてもFAILするリスクがあることに注意


class TestGoogleBooksRepository:
    def setup_method(self, _):
        self.api_client = GoogleBooksRepository()

    def teardown_method(self, _):
        pass

    def test_正確にタイトルを指定して検索結果が得られること(self):
        target_title = "仕事ではじめる機械学習"

        result = self.api_client.search_book_by_title(target_title)

        assert len(result) > 0

        target_books = [x for x in result if x["title"] == target_title]
        assert len(target_books) == 1

        target_book = target_books[0]
        assert target_book["isbn"] == "9784873118253"
        assert target_book["authors"] is not None

        assert isinstance(target_book["authors"], list)
        assert len(target_book["authors"]) == 3

        # テストを実行する場所により "com"と"co.jp"が変わるのでそれ以外の部分のみ比較することにする
        assert target_book["google_books_url"].startswith("http://books.google")
        assert target_book["google_books_url"].endswith(
            "books?id=q0YntAEACAAJ&dq=intitle:%E4%BB%95%E4%BA%8B%E3%81%A7%E3%81%AF%E3%81%98%E3%82%81%E3%82%8B%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92&hl=&source=gbs_api"
        )
        assert target_book["image_url"].startswith("http://books.google")
        assert target_book["image_url"].endswith(
            "books/content?id=q0YntAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
        )
        assert target_book["description"].startswith(
            "機械学習やデータ分析の道具をどのようにビジネスに生かしていけば良いのか、「仕事で使う」という観点から整理。"
        )

    def test_曖昧にタイトルを指定して検索結果が得られること(self):
        target_title = "仕事ではじめる"

        result = self.api_client.search_book_by_title(target_title)

        assert len(result) > 0

    def test_曖昧に複数の単語を指定して検索結果が得られること(self):
        target_title = "仕事 機械学習"

        result = self.api_client.search_book_by_title(target_title)

        assert len(result) > 0

    def test_13桁の正当なISBNを指定したら結果が1件だけ得られること(self):  # pylint: disable=invalid-name
        target_isbn = "9784873118253"

        result = self.api_client.search_book_by_isbn(target_isbn)

        assert result is not None
        assert result["title"] == "仕事ではじめる機械学習"
        assert result["authors"] is not None
        assert result["isbn"] == target_isbn

        # テストを実行する場所により "com"と"co.jp"が変わるのでそれ以外の部分のみ比較することにする
        assert result["google_books_url"].startswith("http://books.google")
        assert result["google_books_url"].endswith(
            "books?id=q0YntAEACAAJ&dq=isbn:9784873118253&hl=&source=gbs_api"
        )
        assert result["image_url"].startswith("http://books.google")
        assert result["image_url"].endswith(
            "books/content?id=q0YntAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
        )
        assert result["description"].startswith(
            "機械学習やデータ分析の道具をどのようにビジネスに生かしていけば良いのか、「仕事で使う」という観点から整理。"
        )

    def test_10桁の正当なISBNを指定したら結果が1件だけ得られること(self):  # pylint: disable=invalid-name
        target_isbn = "4873118255"

        result = self.api_client.search_book_by_isbn(target_isbn)

        assert len(result) is not None
        assert result["title"] == "仕事ではじめる機械学習"
        assert result["authors"] is not None
        assert result["isbn"] == target_isbn

        # テストを実行する場所により "com"と"co.jp"が変わるのでそれ以外の部分のみ比較することにする
        assert result["google_books_url"].startswith("http://books.google")
        assert result["google_books_url"].endswith(
            "books?id=q0YntAEACAAJ&dq=isbn:4873118255&hl=&source=gbs_api"
        )
        assert result["image_url"].startswith("http://books.google")
        assert result["image_url"].endswith(
            "books/content?id=q0YntAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
        )
        assert result["description"].startswith(
            "機械学習やデータ分析の道具をどのようにビジネスに生かしていけば良いのか、「仕事で使う」という観点から整理。"
        )

    def test_存在しないISBNを指定したら結果が0件であること(self):  # pylint: disable=invalid-name
        target_isbn = "1234567890123"

        result = self.api_client.search_book_by_isbn(target_isbn)

        assert result is None

    def test_13桁ではない不正なISBNを指定したら結果が0件であること(self):  # pylint: disable=invalid-name
        target_isbn = "123"

        result = self.api_client.search_book_by_isbn(target_isbn)

        assert result is None
