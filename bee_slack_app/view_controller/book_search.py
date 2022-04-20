def book_search_controller(app):
    @app.action("book_search")
    def open_book_search(ack, body, client):
        # 受信した旨を 3 秒以内に Slack サーバーに伝えます
        ack()
        print("book")
        client.views_push(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                # ビューの識別子
                "callback_id": "view_book_search",
                "title": {"type": "plain_text", "text": "本の検索結果"},
                "submit": {"type": "plain_text", "text": "選択"},
                "blocks": [
                    {
                        "type": "section",
                        "text": {"type": "plain_text", "text": "仕事ではじめる機械学習"},
                    },
                    {
                        "type": "section",
                        "text": {"type": "plain_text", "text": "12345"},
                    },
                ],
            },
        )

    # view_submission リクエストを処理
    @app.view("view_book_search")
    def handle_submission(ack, body, _, view, logger):
        print("検索ボタンからのイベント")

        book_title = view["state"]["values"]["input_book_title"][
            "action_id_book_title"
        ]["value"]
        print(f"Book title= {book_title}")
        isbn = view["state"]["values"]["input_isbn"]["action_id_isbn"]["value"]
        print(f"ISBN code= {isbn}")

        user_id = body["user"]["id"]
        print("user_id:", user_id)

        # view_submission リクエストの確認を行い、モーダルを閉じる
        ack()
