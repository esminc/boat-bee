# pylint: disable=non-ascii-name


from bee_slack_app.repository.book_repository import BookRepository
from bee_slack_app.service.book import book_service


def test_get_booksで本を取得できること_全件取得の場合(mocker):
    mock_book_repository_fetch = mocker.patch.object(
        BookRepository,
        "fetch",
    )
    mock_book_repository_fetch.return_value = {
        "items": [
            {
                "isbn": "3456789012346",
                "title": "dummy_title_2",
                "author": "dummy_author_2",
                "url": "dummy_url_2",
                "image_url": "dummy_image_url_2",
                "updated_at": "2022-04-03T00:00:00+09:00",
            },
            {
                "isbn": "2345678901234",
                "title": "dummy_title_1",
                "author": "dummy_author_1",
                "url": "dummy_url_1",
                "image_url": "dummy_image_url_1",
                "updated_at": "2022-04-02T00:00:00+09:00",
            },
            {
                "isbn": "1234567890123",
                "title": "dummy_title_0",
                "author": "dummy_author_0",
                "url": "dummy_url_0",
                "image_url": "dummy_image_url_0",
                "updated_at": "2022-04-01T00:00:00+09:00",
            },
        ],
        "last_key": None,
    }

    books = book_service.get_books()

    books_items = books["items"]
    books_keys = books["keys"]
    books_has_next = books["has_next"]

    assert len(books_items) == 3
    assert books_keys == ["end"]
    assert books_has_next is False

    assert books_items[0]["isbn"] == "3456789012346"
    assert books_items[0]["title"] == "dummy_title_2"
    assert books_items[0]["author"] == "dummy_author_2"
    assert books_items[0]["url"] == "dummy_url_2"
    assert books_items[0]["image_url"] == "dummy_image_url_2"
    assert books_items[0]["updated_at"] == "2022-04-03T00:00:00+09:00"

    assert books_items[1]["isbn"] == "2345678901234"
    assert books_items[1]["title"] == "dummy_title_1"
    assert books_items[1]["author"] == "dummy_author_1"
    assert books_items[1]["url"] == "dummy_url_1"
    assert books_items[1]["image_url"] == "dummy_image_url_1"
    assert books_items[1]["updated_at"] == "2022-04-02T00:00:00+09:00"

    assert books_items[2]["isbn"] == "1234567890123"
    assert books_items[2]["title"] == "dummy_title_0"
    assert books_items[2]["author"] == "dummy_author_0"
    assert books_items[2]["url"] == "dummy_url_0"
    assert books_items[2]["image_url"] == "dummy_image_url_0"
    assert books_items[2]["updated_at"] == "2022-04-01T00:00:00+09:00"


def test_get_booksで本を取得できること_続きのデータなしの場合(mocker):
    mock_book_repository_fetch = mocker.patch.object(
        BookRepository,
        "fetch",
    )
    mock_book_repository_fetch.return_value = {
        "items": [
            {
                "isbn": "3456789012346",
                "title": "dummy_title_2",
                "author": "dummy_author_2",
                "url": "dummy_url_2",
                "image_url": "dummy_image_url_2",
                "updated_at": "2022-04-03T00:00:00+09:00",
            },
            {
                "isbn": "2345678901234",
                "title": "dummy_title_1",
                "author": "dummy_author_1",
                "url": "dummy_url_1",
                "image_url": "dummy_image_url_1",
                "updated_at": "2022-04-02T00:00:00+09:00",
            },
            {
                "isbn": "1234567890123",
                "title": "dummy_title_0",
                "author": "dummy_author_0",
                "url": "dummy_url_0",
                "image_url": "dummy_image_url_0",
                "updated_at": "2022-04-01T00:00:00+09:00",
            },
        ],
        "last_key": None,
    }

    books = book_service.get_books(limit=3, keys=["dummy_key_0", "dummy_key_1"])

    books_items = books["items"]
    books_keys = books["keys"]
    books_has_next = books["has_next"]

    assert len(books_items) == 3
    assert books_keys == ["dummy_key_0", "dummy_key_1", "end"]
    assert books_has_next is False

    assert books_items[0]["isbn"] == "3456789012346"
    assert books_items[0]["title"] == "dummy_title_2"
    assert books_items[0]["author"] == "dummy_author_2"
    assert books_items[0]["url"] == "dummy_url_2"
    assert books_items[0]["image_url"] == "dummy_image_url_2"
    assert books_items[0]["updated_at"] == "2022-04-03T00:00:00+09:00"

    assert books_items[1]["isbn"] == "2345678901234"
    assert books_items[1]["title"] == "dummy_title_1"
    assert books_items[1]["author"] == "dummy_author_1"
    assert books_items[1]["url"] == "dummy_url_1"
    assert books_items[1]["image_url"] == "dummy_image_url_1"
    assert books_items[1]["updated_at"] == "2022-04-02T00:00:00+09:00"

    assert books_items[2]["isbn"] == "1234567890123"
    assert books_items[2]["title"] == "dummy_title_0"
    assert books_items[2]["author"] == "dummy_author_0"
    assert books_items[2]["url"] == "dummy_url_0"
    assert books_items[2]["image_url"] == "dummy_image_url_0"
    assert books_items[2]["updated_at"] == "2022-04-01T00:00:00+09:00"


def test_get_booksで本を取得できること_続きのデータありの場合(mocker):
    mock_book_repository_fetch = mocker.patch.object(
        BookRepository,
        "fetch",
    )
    mock_book_repository_fetch.return_value = {
        "items": [
            {
                "isbn": "3456789012346",
                "title": "dummy_title_2",
                "author": "dummy_author_2",
                "url": "dummy_url_2",
                "image_url": "dummy_image_url_2",
                "updated_at": "2022-04-03T00:00:00+09:00",
            },
            {
                "isbn": "2345678901234",
                "title": "dummy_title_1",
                "author": "dummy_author_1",
                "url": "dummy_url_1",
                "image_url": "dummy_image_url_1",
                "updated_at": "2022-04-02T00:00:00+09:00",
            },
            {
                "isbn": "1234567890123",
                "title": "dummy_title_0",
                "author": "dummy_author_0",
                "url": "dummy_url_0",
                "image_url": "dummy_image_url_0",
                "updated_at": "2022-04-01T00:00:00+09:00",
            },
        ],
        "last_key": "dummy_last_key",
    }

    books = book_service.get_books(limit=3, keys=["dummy_key_0", "dummy_key_1"])

    books_items = books["items"]
    books_keys = books["keys"]
    books_has_next = books["has_next"]

    assert len(books_items) == 3
    assert books_keys == ["dummy_key_0", "dummy_key_1", "dummy_last_key"]
    assert books_has_next is True

    assert books_items[0]["isbn"] == "3456789012346"
    assert books_items[0]["title"] == "dummy_title_2"
    assert books_items[0]["author"] == "dummy_author_2"
    assert books_items[0]["url"] == "dummy_url_2"
    assert books_items[0]["image_url"] == "dummy_image_url_2"
    assert books_items[0]["updated_at"] == "2022-04-03T00:00:00+09:00"

    assert books_items[1]["isbn"] == "2345678901234"
    assert books_items[1]["title"] == "dummy_title_1"
    assert books_items[1]["author"] == "dummy_author_1"
    assert books_items[1]["url"] == "dummy_url_1"
    assert books_items[1]["image_url"] == "dummy_image_url_1"
    assert books_items[1]["updated_at"] == "2022-04-02T00:00:00+09:00"

    assert books_items[2]["isbn"] == "1234567890123"
    assert books_items[2]["title"] == "dummy_title_0"
    assert books_items[2]["author"] == "dummy_author_0"
    assert books_items[2]["url"] == "dummy_url_0"
    assert books_items[2]["image_url"] == "dummy_image_url_0"
    assert books_items[2]["updated_at"] == "2022-04-01T00:00:00+09:00"


def test_get_booksでbook_repositoryの処理でエラーが発生した場合Noneを返すこと(
    mocker,
):  # pylint: disable=invalid-name
    mock_book_repository_fetch = mocker.patch.object(
        BookRepository,
        "fetch",
    )
    mock_book_repository_fetch.side_effect = Exception("dummy exception")

    books = book_service.get_books(limit=3, keys=["dummy_key_0", "dummy_key_1"])

    assert books is None


def test_get_books_beforeで本を取得できること_0ページへの遷移の場合(mocker):
    mock_book_repository_fetch = mocker.patch.object(
        BookRepository,
        "fetch",
    )
    mock_book_repository_fetch.return_value = {
        "items": [
            {
                "isbn": "3456789012346",
                "title": "dummy_title_2",
                "author": "dummy_author_2",
                "url": "dummy_url_2",
                "image_url": "dummy_image_url_2",
                "updated_at": "2022-04-03T00:00:00+09:00",
            },
            {
                "isbn": "2345678901234",
                "title": "dummy_title_1",
                "author": "dummy_author_1",
                "url": "dummy_url_1",
                "image_url": "dummy_image_url_1",
                "updated_at": "2022-04-02T00:00:00+09:00",
            },
            {
                "isbn": "1234567890123",
                "title": "dummy_title_0",
                "author": "dummy_author_0",
                "url": "dummy_url_0",
                "image_url": "dummy_image_url_0",
                "updated_at": "2022-04-01T00:00:00+09:00",
            },
        ],
        "last_key": "dummy_last_key",
    }

    # 0ページ、1ページのkeysがあるので、現在は1ページ
    # この状態で前に遷移すると0ページに遷移する
    books = book_service.get_books_before(limit=3, keys=["dummy_key_0", "dummy_key_1"])

    books_items = books["items"]
    books_keys = books["keys"]
    books_is_move_to_first = books["is_move_to_first"]

    assert len(books_items) == 3
    assert books_keys == ["dummy_last_key"]
    assert books_is_move_to_first is True

    assert books_items[0]["isbn"] == "3456789012346"
    assert books_items[0]["title"] == "dummy_title_2"
    assert books_items[0]["author"] == "dummy_author_2"
    assert books_items[0]["url"] == "dummy_url_2"
    assert books_items[0]["image_url"] == "dummy_image_url_2"
    assert books_items[0]["updated_at"] == "2022-04-03T00:00:00+09:00"

    assert books_items[1]["isbn"] == "2345678901234"
    assert books_items[1]["title"] == "dummy_title_1"
    assert books_items[1]["author"] == "dummy_author_1"
    assert books_items[1]["url"] == "dummy_url_1"
    assert books_items[1]["image_url"] == "dummy_image_url_1"
    assert books_items[1]["updated_at"] == "2022-04-02T00:00:00+09:00"

    assert books_items[2]["isbn"] == "1234567890123"
    assert books_items[2]["title"] == "dummy_title_0"
    assert books_items[2]["author"] == "dummy_author_0"
    assert books_items[2]["url"] == "dummy_url_0"
    assert books_items[2]["image_url"] == "dummy_image_url_0"
    assert books_items[2]["updated_at"] == "2022-04-01T00:00:00+09:00"


def test_get_books_beforeで本を取得できること_1ページ以降への遷移の場合(mocker):
    mock_book_repository_fetch = mocker.patch.object(
        BookRepository,
        "fetch",
    )
    mock_book_repository_fetch.return_value = {
        "items": [
            {
                "isbn": "3456789012346",
                "title": "dummy_title_2",
                "author": "dummy_author_2",
                "url": "dummy_url_2",
                "image_url": "dummy_image_url_2",
                "updated_at": "2022-04-03T00:00:00+09:00",
            },
            {
                "isbn": "2345678901234",
                "title": "dummy_title_1",
                "author": "dummy_author_1",
                "url": "dummy_url_1",
                "image_url": "dummy_image_url_1",
                "updated_at": "2022-04-02T00:00:00+09:00",
            },
            {
                "isbn": "1234567890123",
                "title": "dummy_title_0",
                "author": "dummy_author_0",
                "url": "dummy_url_0",
                "image_url": "dummy_image_url_0",
                "updated_at": "2022-04-01T00:00:00+09:00",
            },
        ],
        "last_key": "dummy_last_key",
    }

    # 0ページ、1ページ、2ページのkeysがあるので、現在は2ページ
    # この状態で前に遷移すると1ページに遷移する
    books = book_service.get_books_before(
        limit=3, keys=["dummy_key_0", "dummy_key_1", "dummy_key_2"]
    )

    books_items = books["items"]
    books_keys = books["keys"]
    books_is_move_to_first = books["is_move_to_first"]

    assert len(books_items) == 3
    assert books_keys == ["dummy_key_0", "dummy_key_1"]
    assert books_is_move_to_first is False

    assert books_items[0]["isbn"] == "3456789012346"
    assert books_items[0]["title"] == "dummy_title_2"
    assert books_items[0]["author"] == "dummy_author_2"
    assert books_items[0]["url"] == "dummy_url_2"
    assert books_items[0]["image_url"] == "dummy_image_url_2"
    assert books_items[0]["updated_at"] == "2022-04-03T00:00:00+09:00"

    assert books_items[1]["isbn"] == "2345678901234"
    assert books_items[1]["title"] == "dummy_title_1"
    assert books_items[1]["author"] == "dummy_author_1"
    assert books_items[1]["url"] == "dummy_url_1"
    assert books_items[1]["image_url"] == "dummy_image_url_1"
    assert books_items[1]["updated_at"] == "2022-04-02T00:00:00+09:00"

    assert books_items[2]["isbn"] == "1234567890123"
    assert books_items[2]["title"] == "dummy_title_0"
    assert books_items[2]["author"] == "dummy_author_0"
    assert books_items[2]["url"] == "dummy_url_0"
    assert books_items[2]["image_url"] == "dummy_image_url_0"
    assert books_items[2]["updated_at"] == "2022-04-01T00:00:00+09:00"


def test_get_books_beforeでbook_repositoryの処理でエラーが発生した場合Noneを返すこと(
    mocker,
):  # pylint: disable=invalid-name
    mock_book_repository_fetch = mocker.patch.object(
        BookRepository,
        "fetch",
    )
    mock_book_repository_fetch.side_effect = Exception("dummy exception")

    books = book_service.get_books_before(
        limit=3, keys=["dummy_key_0", "dummy_key_1", "dummy_key_2"]
    )

    assert books is None
