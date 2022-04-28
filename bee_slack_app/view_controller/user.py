def user_controller(app):
    @app.action("user_info")
    def open_user_info(ack, body, client):
        # 受信した旨を 3 秒以内に Slack サーバーに伝えます
        ack()

        client.views_open(
            trigger_id=body["trigger_id"],
            # ビューのペイロード
            view={
                "type": "modal",
                # ビューの識別子
                "callback_id": "user",
                "title": {"type": "plain_text", "text": "プロフィール"},
                "submit": {"type": "plain_text", "text": "登録", "emoji": True},
                "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
                "blocks": [
                    {
                        "type": "input",
                        "block_id": "input_user_name",
                        "label": {"type": "plain_text", "text": "氏名"},
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "plain_text_input-action",
                        },
                    },
                    {
                        "type": "input",
                        "block_id": "input_department",
                        "label": {"type": "plain_text", "text": "所属事業部"},
                        "element": {
                            "type": "static_select",
                            "action_id": "action_id_department",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "選択してください",
                                "emoji": True,
                            },
                            "options": [
                                {
                                    "value": "0",
                                    "text": {"type": "plain_text", "text": "ITS事業部"},
                                },
                                {
                                    "value": "1",
                                    "text": {"type": "plain_text", "text": "金融システム事業部"},
                                },
                                {
                                    "value": "2",
                                    "text": {"type": "plain_text", "text": "医療システム事業部"},
                                },
                                {
                                    "value": "3",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "アジャイルシステム事業部",
                                    },
                                },
                                {
                                    "value": "4",
                                    "text": {"type": "plain_text", "text": "管理部"},
                                },
                            ],
                        },
                    },
                    {
                        "type": "input",
                        "block_id": "input_job_type",
                        "label": {"type": "plain_text", "text": "職種"},
                        "element": {
                            "type": "static_select",
                            "action_id": "action_id_job_type",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "選択してください",
                                "emoji": True,
                            },
                            "options": [
                                {
                                    "value": "value-0",
                                    "text": {"type": "plain_text", "text": "エンジニア"},
                                },
                                {
                                    "value": "value-1",
                                    "text": {"type": "plain_text", "text": "管理職"},
                                },
                                {
                                    "value": "value-2",
                                    "text": {"type": "plain_text", "text": "営業"},
                                },
                            ],
                        },
                    },
                    {
                        "type": "input",
                        "block_id": "input_age_range",
                        "label": {"type": "plain_text", "text": "年代"},
                        "element": {
                            "type": "static_select",
                            "action_id": "action_id_age_range",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "選択してください",
                                "emoji": True,
                            },
                            "options": [
                                {
                                    "value": "value-0",
                                    "text": {"type": "plain_text", "text": "20代"},
                                },
                                {
                                    "value": "value-1",
                                    "text": {"type": "plain_text", "text": "30代"},
                                },
                                {
                                    "value": "value-2",
                                    "text": {"type": "plain_text", "text": "40代"},
                                },
                                {
                                    "value": "value-3",
                                    "text": {"type": "plain_text", "text": "50代"},
                                },
                                {
                                    "value": "value-4",
                                    "text": {"type": "plain_text", "text": "60代"},
                                },
                            ],
                        },
                    },
                ],
            },
        )
