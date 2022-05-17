# pylint: disable=non-ascii-name

from logging import getLogger

from bee_slack_app.model.search import SearchedBook
from bee_slack_app.model.user import User
from bee_slack_app.service.recommend import recommend


def test_おすすめの本の情報を取得できること(monkeypatch):
    user: User = {}
    user["user_id"] = ("U03B49AKZV4",)
    user["user_name"] = ("三田村岳周",)
    user["department"] = ("finance",)
    user["job_type"] = ("engineer",)
    user["age_range"] = ("60",)
    user["age_range"] = ("2022-05-17T10:07:25+09:00",)

    logger = getLogger
    book: SearchedBook = recommend(logger, user)

    assert book["title"] == "仕事ではじめる機械学習"
    assert book["isbn"] == "9784873118253"
    assert book["author"] == ["有賀康顕", "中山心太", "西林孝"]
    assert (
        book["image_url"]
        == "http://books.google.com/books/content?id=q0YntAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
    )
    assert (
        book["google_books_url"]
        == "http://books.google.co.jp/books?id=q0YntAEACAAJ&dq=isbn:9784873118253&hl=&source=gbs_api"
    )


# def test_おすすめの本の情報がNoneのケース(monkeypatch):


# def test_おすすめ本の著者が複数人でも全員が返値に設定されること(monkeypatch):


# def test_おすすめ本の書影がNoneならダミーの書影が返値に設定されること(monkeypatch):


# def test_おすすめ本を取得するユーザーが存在しない場合は返値はNoneであること(monkeypatch):


# def test_モジュール内で例外が発生した場合は返値はNoneであること(monkeypatch):
