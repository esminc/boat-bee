from bee_slack_app.view_controller.review import open_new_modal


def book_search_controller(app):
    @app.action("book_search")
    def open_book_search(ack, body, client):
        # 受信した旨を 3 秒以内に Slack サーバーに伝えます
        ack()

        search_item1 = {
            "value": "12345",
            "text": {
                "type": "plain_text",
                "text": "仕事ではじめる機械学習",
                "emoji": True,
            },
        }
        search_item2 = {
            "value": "11111",
            "text": {
                "type": "plain_text",
                "text": "機械学習",
                "emoji": True,
            },
        }
        search_item3 = {
            "value": "88888",
            "text": {
                "type": "plain_text",
                "text": "機械学習図鑑",
                "emoji": True,
            },
        }

        search_list = []
        # PRマージ後にfor文に修正する。
        # for _ in range(3):
        search_list.append(search_item1)
        search_list.append(search_item2)
        search_list.append(search_item3)

        client.views_push(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                # ビューの識別子
                "callback_id": "view_book_search",
                "title": {"type": "plain_text", "text": "本の検索結果", "emoji": True},
                "submit": {"type": "plain_text", "text": "選択", "emoji": True},
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
    def handle_submission(ack, _, __, view):
        book_title = view["state"]["values"]["book_select"]["radio_buttons-action"][
            "selected_option"
        ]["text"]["text"]
        isbn = view["state"]["values"]["book_select"]["radio_buttons-action"][
            "selected_option"
        ]["value"]

        # view_submission リクエストの確認を行い、モーダルを閉じる
        ack(response_action="update", view=open_new_modal(book_title, isbn))
