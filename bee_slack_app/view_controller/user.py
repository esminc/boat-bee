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
                        "type": "section",
                        "block_id": "section_user_name",
                        "text": {
                            "type": "plain_text",
                            # TODO: SlackのユーザIDからSlackの表示名を取得して表示する
                            "text": "えいわ　たろう（今は初期値として固定表示）",
                        },
                    },
                    {
                        "type": "input",
                        "block_id": "input_department",
                        "label": {"type": "plain_text", "text": "事業部"},
                        "element": {
                            "type": "static_select",
                            "action_id": "action_id_department",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "事業部を選択してください",
                                "emoji": True,
                            },
                            "options": [
                                {
                                    "value": "its",
                                    "text": {"type": "plain_text", "text": "ITS事業部"},
                                },
                                {
                                    "value": "finance",
                                    "text": {"type": "plain_text", "text": "金融システム事業部"},
                                },
                                {
                                    "value": "medical",
                                    "text": {"type": "plain_text", "text": "医療システム事業部"},
                                },
                                {
                                    "value": "agile",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "アジャイルシステム事業部",
                                    },
                                },
                                {
                                    "value": "general",
                                    "text": {"type": "plain_text", "text": "管理部"},
                                },
                                {
                                    "value": "other",
                                    "text": {"type": "plain_text", "text": "その他"},
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
                                "text": "職種を選択してください",
                                "emoji": True,
                            },
                            "options": [
                                {
                                    "value": "engineer",
                                    "text": {"type": "plain_text", "text": "エンジニア"},
                                },
                                {
                                    "value": "management",
                                    "text": {"type": "plain_text", "text": "管理職"},
                                },
                                {
                                    "value": "sales",
                                    "text": {"type": "plain_text", "text": "営業"},
                                },
                                {
                                    "value": "other",
                                    "text": {"type": "plain_text", "text": "その他"},
                                },
                            ],
                        },
                    },
                    {
                        "type": "input",
                        "block_id": "input_age_range",
                        "label": {"type": "plain_text", "text": "年齢層"},
                        "element": {
                            "type": "static_select",
                            "action_id": "action_id_age_range",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "年齢層を選択してください",
                                "emoji": True,
                            },
                            "options": [
                                {
                                    "value": "10",
                                    "text": {"type": "plain_text", "text": "～19才"},
                                },
                                {
                                    "value": "20",
                                    "text": {"type": "plain_text", "text": "20才～29才"},
                                },
                                {
                                    "value": "30",
                                    "text": {"type": "plain_text", "text": "30才～39才"},
                                },
                                {
                                    "value": "40",
                                    "text": {"type": "plain_text", "text": "40才～49才"},
                                },
                                {
                                    "value": "50",
                                    "text": {"type": "plain_text", "text": "50才～59才"},
                                },
                                {
                                    "value": "60",
                                    "text": {"type": "plain_text", "text": "60才～"},
                                },
                            ],
                        },
                    },
                ],
            },
        )
