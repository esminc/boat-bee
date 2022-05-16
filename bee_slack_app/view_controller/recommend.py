from typing import Optional

from bee_slack_app.model.search import SearchedBook
from bee_slack_app.model.user import User
from bee_slack_app.service.user import get_user


def recommend_controller(app):  # pylint: disable=too-many-statements
    @app.action("book_recommend")
    def open_recommmend_modal(ack, body, client, logger):
        # コマンドのリクエストを確認
        ack()
        logger.info(body)

        user_id = body["user"]["id"]

        user: Optional[User] = get_user(logger, user_id)
        if not user:
            client.views_open(
                trigger_id=body["trigger_id"],
                view={
                    "type": "modal",
                    "title": {
                        "type": "plain_text",
                        "text": "プロフィールを入力してください",
                        "emoji": True,
                    },
                    "close": {"type": "plain_text", "text": "OK", "emoji": True},
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "おすすめ本を見るには、プロフィールの入力が必要です :bow:",
                            },
                        },
                    ],
                },
            )
            return

        # TODO レコメンドのサービスから、おすすめのブック情報を取得する
        # いまはモックでブック情報を代入する
        book: SearchedBook = {
            "title": "道は開ける",
            "isbn": "9784422100999",
            "author": "デールカーネギー",
            "image_url": "http://books.google.com/books/content?id=rfVbjwEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api",
            "google_books_url": "http://books.google.co.jp/books?id=rfVbjwEACAAJ&dq=isbn:9784422100999&hl=&source=gbs_api",
        }

        if book is None:
            client.views_open(
                trigger_id=body["trigger_id"],
                view={
                    "type": "modal",
                    "title": {
                        "type": "plain_text",
                        "text": "おすすめの本は見つかりませんでした",
                        "emoji": True,
                    },
                    "close": {"type": "plain_text", "text": "OK", "emoji": True},
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "アプリ管理者にお問い合わせください :bow:",
                            },
                        },
                    ],
                },
            )
            return

        # TODO: 暫定で適当な画像をデフォルトに設定、S3に画像を置くようになったら自前の画像に差し替える
        dummy_url = "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg"

        author = ", ".join(book["author"])
        image_url = book["image_url"] if book["image_url"] is not None else dummy_url

        modal_view = generate_book_recommend_model_view(book, author, image_url)

        client.views_open(
            trigger_id=body["trigger_id"],
            # ビューのペイロード
            view=modal_view,
        )

    def generate_book_recommend_model_view(
        book: Optional[SearchedBook], author, image_url
    ):

        view = {
            "type": "modal",
            "callback_id": "book_recommend",
            "title": {"type": "plain_text", "text": "あなたへのおすすめ本"},
            "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{book['title']}*\n{author}\nISBN-{book['isbn']}",
                        # "text": f"*{book['title']}*\n{book['author']}\nISBN-{book['isbn']}",
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": image_url,
                        "alt_text": "Windsor Court Hotel thumbnail",
                    },
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Google Booksで見る",
                                "emoji": True,
                            },
                            "url": book["google_books_url"],
                            "action_id": "google_books_buttons-action",
                        },
                    ],
                },
                {
                    "type": "image",
                    "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
                    "alt_text": "",
                },
            ],
        }
        return view
