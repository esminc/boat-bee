from typing import Optional

from bee_slack_app.model.search import SearchedBook
from bee_slack_app.model.user import User
from bee_slack_app.service.book_search import search_book_by_isbn
from bee_slack_app.service.user import get_user


def recommend_controller(app):  # pylint: disable=too-many-statements
    @app.action("book_recommend")
    def open_recommmend_modal(ack, body, client, logger):
        # コマンドのリクエストを確認
        ack()
        logger.info(body)

        user_id = body["user"]["id"]
        print("user_id = " + user_id)

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

        print(user)

        # TODO レコメンドのサービスから、レコメンド情報を取得する
        # おすすめ度（recommend_score）をモックで入れる
        recommend_score: str = "3.5"
        # いまはisbnをモックで代入する
        isbn = "9784422100999"

        # レコメンド情報のisbnから本の情報を取得する
        book = search_book_by_isbn(isbn)

        # TODO 対象のbookがisbnから見つからなかった場合の処理

        # TODO: 暫定で適当な画像をデフォルトに設定、S3に画像を置くようになったら自前の画像に差し替える
        dummy_url = "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg"

        author = ", ".join(book["author"])
        image_url = book["image_url"] if book["image_url"] is not None else dummy_url

        modal_view = generate_book_recommend_model_view(
            book, author, image_url, recommend_score
        )

        client.views_open(
            trigger_id=body["trigger_id"],
            # ビューのペイロード
            view=modal_view,
        )

    def generate_book_recommend_model_view(
        book: Optional[SearchedBook], author, image_url, recommend_score
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
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": image_url,
                        "alt_text": "Windsor Court Hotel thumbnail",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "おすすめ度は " + recommend_score + " です",
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
