# pylint: disable=duplicate-code


def book_controller(app):
    def respond_to_slack_within_3_seconds(body, ack):
        ack()

    def open_see_more_recommended_book_modal(body, client):
        """
        あなたへのおすすめ本モーダル
        """
        client.views_open(
            trigger_id=body["trigger_id"],
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

    app.action("see_more_recommended_book")(
        # この場合でも ack() は 3 秒以内に呼ばれます
        ack=respond_to_slack_within_3_seconds,
        # Lazy 関数がイベントの処理を担当します
        lazy=[open_see_more_recommended_book_modal],
    )
