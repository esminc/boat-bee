from typing import Optional

from bee_slack_app.model.search import SearchedBook
from bee_slack_app.model.user import User
from bee_slack_app.service.recommend import recommend
from bee_slack_app.service.user import get_user


def recommend_controller(app):  # pylint: disable=too-many-statements
    @app.action("book_recommend")
    def open_recommend_modal(ack, body, client, logger):
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

        book: Optional[SearchedBook] = recommend(logger, user)

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

        modal_view = generate_book_recommend_model_view(book)

        client.views_open(
            trigger_id=body["trigger_id"],
            # ビューのペイロード
            view=modal_view,
        )

    def generate_book_recommend_model_view(book: SearchedBook):
        # TODO: 暫定で適当な画像をデフォルトに設定、S3に画像を置くようになったら自前の画像に差し替える
        dummy_url = "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg"
        image_url = book["image_url"] if book["image_url"] is not None else dummy_url
        authors = ", ".join(book["authors"])

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
                        "text": f"*{book['title']}*\n{authors}\nISBN-{book['isbn']}",
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": image_url,
                        "alt_text": "An incredibly cute kitten.",
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
