def book_search_controller(app):
    @app.action("book_search")
    def open_book_search(ack, body, client):
        # 受信した旨を 3 秒以内に Slack サーバーに伝えます
        ack()

        search_item = {
            "value": "12345",
            "text": {
                "type": "plain_text",
                "text": "仕事ではじめる機械学習",
                "emoji": True,
            },
        }

        search_list = []
        for _ in range(3):
            search_list.append(search_item)

        client.views_push(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                # ビューの識別子
                "callback_id": "view_book_search",
                "title": {"type": "plain_text", "text": "本の検索結果", "emoji": True},
                "submit": {"type": "plain_text", "text": "選択", "emoji": True},
                # sumを使って2次元配列を平坦化
                "blocks": [
                    {
                        "type": "input",
                        "block_id": "book_select",
                        "element": {
                            "type": "radio_buttons",
                            "options": search_list,
                            "action_id": "radio_buttons-action",
                        },
                        "label": {"type": "plain_text", "text": "Label", "emoji": True},
                    },
                ],
            },
        )

    # view_submission リクエストを処理
    @app.view("view_book_search")
    def handle_submission(ack, body, _, view, logger, payload):
        print(
            "book_select:",
            view["state"]["values"]["book_select"]["radio_buttons-action"],
        )

        book_title = view["state"]["values"]["book_select"]["radio_buttons-action"][
            "selected_option"
        ]["text"]["text"]
        print(f"Book title= {book_title}")
        isbn = view["state"]["values"]["book_select"]["radio_buttons-action"][
            "selected_option"
        ]["value"]
        print(f"ISBN code= {isbn}")

        user_id = body["user"]["id"]
        print("user_id:", user_id)

        # view_submission リクエストの確認を行い、モーダルを閉じる
        ack(response_action="update", view=build_new_view(book_title, isbn))


def build_new_view(book_title, isbn):
    print("-----build_new_view-----")
    print("book_title:", book_title)
    print("isbn:", isbn)
    view = {
        "type": "modal",
        # ビューの識別子
        "callback_id": "view_1",
        "title": {"type": "plain_text", "text": "Bee"},
        "submit": {"type": "plain_text", "text": "送信"},
        "blocks": [
            {
                "type": "input",
                "block_id": "input_book_title",
                "label": {"type": "plain_text", "text": "タイトル"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "action_id_book_title",
                    "initial_value": book_title,
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "本の検索"},
                        "action_id": "book_search",
                    },
                ],
            },
            {
                "type": "input",
                "block_id": "input_isbn",
                "label": {"type": "plain_text", "text": "ISBN Code"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "action_id_isbn",
                    "initial_value": isbn,
                },
            },
            {
                "type": "input",
                "block_id": "input_score_for_me",
                "label": {"type": "plain_text", "text": "自分にとっての評価"},
                "element": {
                    "type": "radio_buttons",
                    "action_id": "action_id_score_for_me",
                    "initial_option": {
                        "value": "3",
                        "text": {"type": "plain_text", "text": "普通"},
                    },
                    "options": [
                        {
                            "value": "5",
                            "text": {"type": "plain_text", "text": "とても良い"},
                        },
                        {
                            "value": "4",
                            "text": {"type": "plain_text", "text": "良い"},
                        },
                        {
                            "value": "3",
                            "text": {"type": "plain_text", "text": "普通"},
                        },
                        {
                            "value": "2",
                            "text": {"type": "plain_text", "text": "悪い"},
                        },
                        {
                            "value": "1",
                            "text": {"type": "plain_text", "text": "とても悪い"},
                        },
                    ],
                },
            },
            {
                "type": "input",
                "block_id": "input_score_for_others",
                "label": {"type": "plain_text", "text": "他の人へのお勧め度"},
                "element": {
                    "type": "radio_buttons",
                    "action_id": "action_id_score_for_others",
                    "initial_option": {
                        "value": "3",
                        "text": {"type": "plain_text", "text": "普通"},
                    },
                    "options": [
                        {
                            "value": "5",
                            "text": {"type": "plain_text", "text": "とてもお勧め"},
                        },
                        {
                            "value": "4",
                            "text": {"type": "plain_text", "text": "お勧め"},
                        },
                        {
                            "value": "3",
                            "text": {"type": "plain_text", "text": "普通"},
                        },
                        {
                            "value": "2",
                            "text": {"type": "plain_text", "text": "お勧めしない"},
                        },
                        {
                            "value": "1",
                            "text": {"type": "plain_text", "text": "絶対にお勧めしない"},
                        },
                    ],
                },
            },
            {
                "type": "input",
                "block_id": "input_comment",
                "label": {"type": "plain_text", "text": "レビューコメント"},
                "optional": True,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "action_id_comment",
                    "multiline": True,
                },
            },
        ],
    }
    print("view:", view)

    return view
