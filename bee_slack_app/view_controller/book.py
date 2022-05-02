# pylint: disable=duplicate-code


def book_controller(app):
    @app.action("see_more_recommended_book")
    def open_see_more_recommended_book_modal(ack, body, client):
        """
        あなたへのおすすめ本モーダル
        """
        ack()
        client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "title": {"type": "plain_text", "text": "あなたへのおすすめ本", "emoji": True},
                "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "ウェブ最適化ではじめる機械学習",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "image",
                        "image_url": "http://books.google.com/books/content?id=jQ0OzgEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api",
                        "alt_text": "ウェブ最適化ではじめる機械学習",
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": "*著者*\n飯塚修平"},
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": "*ISBN*\n9784873119168"},
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "<https://books.google.co.jp/books?id=jQ0OzgEACAAJ&dq=webæé©å&hl=&source=gbs_api|Google Booksで見る>",
                        },
                    },
                ],
            },
        )
