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
                            "text": "読書レビュー共有アプリ「Bee（Book Erabu Eiwa）」",
                            "emoji": True,
                        },
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*読んだ本のレビューを投稿して、データ蓄積に協力お願いします* ",
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Beeは、FDOが開発・提供する、本のレビュー共有アプリです。\n仕事で役立った本のレビューを投稿・共有できます。\nデータがたまればたまるほど、AIはより賢くなりあなたに合ったおすすめの本をお伝えすることができます。\n書籍購入制度で購入した本などのレビューを投稿してみましょう！！。",
                        },
                    },
                    {"type": "divider"},
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
                                "action_id": "book_recommend",
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
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": "ユーザ情報", "emoji": True},
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "プロフィール",
                                    "emoji": True,
                                },
                                "value": "dummy_value",
                                "action_id": "user_info",
                            },
                        ],
                    },
                ],
            },
        )
