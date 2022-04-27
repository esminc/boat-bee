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
            view_id=body["view"]["id"],
            hash=body["view"]["hash"],
            view={
                "type": "modal",
                "title": {"type": "plain_text", "text": "あなたへのおすすめ本", "emoji": True},
                "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "ごめんなさい :bow: \nここは未実装です!!\n\nみなさんのレビューがたまれば、\nそれを元に、あなたにおすすめの本を表示します!!",
                        },
                    }
                ],
            },
        )