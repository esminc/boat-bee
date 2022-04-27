def home_controller(app):
    @app.event("app_home_opened")
    def update_home_view(ack, event, client):
        ack()

        client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "あなたへのおすすめ本",
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
                        "text": {"type": "plain_text", "text": "本のレビュー", "emoji": True},
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
