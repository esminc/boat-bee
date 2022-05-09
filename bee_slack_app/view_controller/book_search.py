import json

from bee_slack_app.service.book_search import search_book_by_title
from bee_slack_app.view_controller.review import generate_review_input_modal_view


def book_search_controller(app):
    @app.action("book_search")
    def open_book_search(ack, body, client):
        """
        検索結果のモーダルを開く
        """
        # 受信した旨を 3 秒以内に Slack サーバーに伝えます
        ack()

        title = body["view"]["state"]["values"]["input_book_title"][
            "action_id_book_title"
        ]["value"]

        if title is None:
            client.views_push(
                trigger_id=body["trigger_id"],
                view={
                    "type": "modal",
                    "title": {"type": "plain_text", "text": "エラー", "emoji": True},
                    "close": {"type": "plain_text", "text": "OK", "emoji": True},
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "plain_text",
                                "text": "本のタイトルが未入力です",
                                "emoji": True,
                            },
                        },
                    ],
                },
            )

        else:
            book_results = search_book_by_title(title)

            if len(book_results) == 0:
                client.views_push(
                    trigger_id=body["trigger_id"],
                    view={
                        "type": "modal",
                        "title": {"type": "plain_text", "text": "検索結果", "emoji": True},
                        "close": {"type": "plain_text", "text": "OK", "emoji": True},
                        "blocks": [
                            {
                                "type": "section",
                                "text": {
                                    "type": "plain_text",
                                    "text": "検索結果が0件でした",
                                    "emoji": True,
                                },
                            },
                        ],
                    },
                )
            else:
                book_result_summary = []

                for book_result in book_results:

                    # ボタン選択時に書籍のデータを再利用するため情報を保持しておく
                    # とりあえずはTitleとISBNを取得できれば良い
                    # private_metadataに格納できる情報が3000文字なので最小限にする
                    book_info = {
                        "isbn": book_result["isbn"],
                        "title": book_result["title"],
                    }
                    book_result_summary.append(book_info)

                # private_metadataに格納するために文字列に変換する
                private_metadata = json.dumps(book_result_summary)

                client.views_push(
                    trigger_id=body["trigger_id"],
                    view=generate_search_result_model_view(
                        book_results=book_results, private_metadata=private_metadata
                    ),
                )

    def generate_search_result_model_view(
        book_results,
        private_metadata: str,
    ):
        """
        検索結果画面の作成を行う
        """

        blocks = []
        for book in book_results:
            blocks.extend(generate_book_block(book))

        view = {
            "type": "modal",
            "callback_id": "view_book_search",
            "private_metadata": private_metadata,
            "title": {
                "type": "plain_text",
                "text": "本の検索結果",
                "emoji": True,
            },
            "submit": {"type": "plain_text", "text": "選択", "emoji": True},
            "blocks": blocks,
        }

        return view

    def generate_book_block(book):
        # TODO: 暫定で適当な画像をデフォルトに設定、S3に画像を置くようになったら自前の画像に差し替える
        dummy_url = "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg"

        author = ", ".join(book["author"])
        image_url = book["image_url"] if book["image_url"] is not None else dummy_url

        block = [
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{book['title']}*\n{author}\nISBN-{book['isbn']}",
                },
                "accessory": {
                    "type": "image",
                    "image_url": image_url,
                    "alt_text": "Windsor Court Hotel thumbnail",
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "選択", "emoji": True},
                        "value": book["isbn"],
                        "action_id": "select_buttons-action",
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Google Booksで見る",
                            "emoji": True,
                        },
                        "url": book["google_books_url"],
                    },
                ],
            },
        ]

        return block

    @app.action("select_buttons-action")
    def handle_book_selected(ack, body, _, client):
        """
        検索結果画面でボタンを選択した時に行う処理
        """

        private_metadata = body["view"]["private_metadata"]

        # private_metadataに格納していた情報を復元する
        search_resut: list = json.loads(private_metadata)

        # private_metadataに選択情報が入っている場合は取り除く
        search_resut = [x for x in search_resut if x.get("isbn", None) is not None]

        isbn = body["actions"][0]["value"]
        title = [x for x in search_resut if x["isbn"] == isbn][0]["title"]

        # private_metadataに選択情報を追加する
        selected_item = {"selected_title": title, "selected_isbn": isbn}
        search_resut.append(selected_item)

        # ボタンの選択状態を更新する
        blocks = body["view"]["blocks"]
        new_blocks = [
            x
            if x["type"] != "actions"
            else selected_book(x)
            if x["elements"][0]["value"] == isbn
            else unselected_book(x)
            for x in blocks
        ]

        new_view = {
            "type": "modal",
            "callback_id": "view_book_search",
            "private_metadata": json.dumps(search_resut),
            "title": {
                "type": "plain_text",
                "text": "本の検索結果",
                "emoji": True,
            },
            "submit": {"type": "plain_text", "text": "選択", "emoji": True},
            "blocks": new_blocks,
        }
        client.views_update(
            view_id=body["container"]["view_id"],
            view=new_view,
        )
        ack()

    def selected_book(item):
        """
        ボタンが選択された本のblockを生成する
        """
        return {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": ":hand:選択中です",
                        "emoji": True,
                    },
                    "value": item["elements"][0]["value"],
                    "action_id": "select_buttons-action",
                    "style": "primary",
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Google Booksで見る",
                        "emoji": True,
                    },
                    "url": item["elements"][1]["url"],
                },
            ],
        }

    def unselected_book(item):
        """
        ボタンが選択されていない本のblockを生成する
        """
        return {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "選択", "emoji": True},
                    "value": item["elements"][0]["value"],
                    "action_id": "select_buttons-action",
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Google Booksで見る",
                        "emoji": True,
                    },
                    "url": item["elements"][1]["url"],
                },
            ],
        }

    # view_submission リクエストを処理
    @app.view("view_book_search")
    def handle_submission(ack, body, _, __):
        """
        検索結果画面で選択ボタンを押下したときに行う処理
        """

        # 通常のボタン押下状態はactionsには入ってこないためprivate_metadataで伝達する
        # private_metadataに格納していたCacheを文字列から復元する
        cache_list = body["view"]["private_metadata"]
        items: list = json.loads(cache_list)

        book = [x for x in items if x.get("selected_title", None) is not None][0]
        title = book["selected_title"]
        isbn = book["selected_isbn"]

        # view_submission リクエストの確認を行い、モーダルを閉じる
        ack(
            response_action="update",
            view=generate_review_input_modal_view(title, isbn),
        )
