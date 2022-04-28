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
                            "action_id": "action_id_department",
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

    #     title = body["view"]["state"]["values"]["input_book_title"][
    #         "action_id_book_title"
    #     ]["value"]

    #     if title is None:

    #         client.views_push(
    #             trigger_id=body["trigger_id"],
    #             view={
    #                 "type": "modal",
    #                 "title": {"type": "plain_text", "text": "エラー", "emoji": True},
    #                 "close": {"type": "plain_text", "text": "OK", "emoji": True},
    #                 "blocks": [
    #                     {
    #                         "type": "section",
    #                         "text": {
    #                             "type": "plain_text",
    #                             "text": "本のタイトルが未入力です",
    #                             "emoji": True,
    #                         },
    #                     },
    #                 ],
    #             },
    #         )

    #     else:
    #         book_results = search_book_by_title(title)

    #         if len(book_results) == 0:
    #             client.views_push(
    #                 trigger_id=body["trigger_id"],
    #                 view={
    #                     "type": "modal",
    #                     "title": {"type": "plain_text", "text": "検索結果", "emoji": True},
    #                     "close": {"type": "plain_text", "text": "OK", "emoji": True},
    #                     "blocks": [
    #                         {
    #                             "type": "section",
    #                             "text": {
    #                                 "type": "plain_text",
    #                                 "text": "検索結果が0件でした",
    #                                 "emoji": True,
    #                             },
    #                         },
    #                     ],
    #                 },
    #             )
    #         else:
    #             search_list = []

    #             for book_result in book_results:
    #                 search_item = {
    #                     "value": book_result["isbn"],
    #                     "text": {
    #                         "type": "plain_text",
    #                         "text": book_result["title"],
    #                         "emoji": True,
    #                     },
    #                 }
    #                 search_list.append(search_item)

    #             client.views_push(
    #                 trigger_id=body["trigger_id"],
    #                 view={
    #                     "type": "modal",
    #                     # ビューの識別子
    #                     "callback_id": "view_book_search",
    #                     "title": {
    #                         "type": "plain_text",
    #                         "text": "本の検索結果",
    #                         "emoji": True,
    #                     },
    #                     "submit": {"type": "plain_text", "text": "選択", "emoji": True},
    #                     "blocks": [
    #                         {
    #                             "type": "input",
    #                             "block_id": "book_select",
    #                             "element": {
    #                                 "type": "radio_buttons",
    #                                 "options": search_list,
    #                                 "action_id": "radio_buttons-action",
    #                             },
    #                             "label": {
    #                                 "type": "plain_text",
    #                                 "text": "選択してください",
    #                                 "emoji": True,
    #                             },
    #                         },
    #                     ],
    #                 },
    #             )

    # # view_submission リクエストを処理
    # @app.view("view_book_search")
    # def handle_submission(ack, _, __, view):
    #     book_title = view["state"]["values"]["book_select"]["radio_buttons-action"][
    #         "selected_option"
    #     ]["text"]["text"]
    #     isbn = view["state"]["values"]["book_select"]["radio_buttons-action"][
    #         "selected_option"
    #     ]["value"]

    #     # view_submission リクエストの確認を行い、モーダルを閉じる
    #     ack(
    #         response_action="update",
    #         view=generate_review_input_modal_view(book_title, isbn),
    #     )
