def home_controller(app):
    @app.command("/bee")
    def open_home_modal(ack, body, client):
        ack()

        client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "title": {"type": "plain_text", "text": "Bee", "emoji": True},
                "type": "modal",
                "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "今日のおすすめ本",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "あなたにおすすめの本は...\n *「仕事ではじめる機械学習」* ",
                        },
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "詳しく見る",
                                    "emoji": True,
                                },
                                "value": "dummy_value",
                                "action_id": "see_more_recommended_book",
                            }
                        ],
                    },
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "本のレビュー",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "レビューを閲覧する :eyes:",
                                    "emoji": True,
                                },
                                "value": "dummy_value",
                                "action_id": "read_review",
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "レビューを投稿する :memo:",
                                    "emoji": True,
                                },
                                "value": "dummy_value",
                                "action_id": "post_review",
                            },
                        ],
                    },
                ],
            },
        )
