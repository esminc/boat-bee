import json

from bee_slack_app.model.search import SearchedBook
from bee_slack_app.service.book_search import search_book_by_title
from bee_slack_app.view_controller.review import generate_review_input_modal_view


def book_search_controller(app):
    @app.view("book_search_modal")
    def open_book_search_result_modal(ack, body):
        """
        検索結果のモーダルを開く
        """
        title = body["view"]["state"]["values"]["input_book_title"][
            "action_id_book_title"
        ]["value"]

        if title is None:
            ack(
                response_action="push",
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
                ack(
                    response_action="push",
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

                ack(
                    response_action="push",
                    view=generate_search_result_model_view(
                        book_results=book_results, private_metadata=private_metadata
                    ),
                )

    def generate_search_result_model_view(
        book_results: list[SearchedBook],
        private_metadata: str,
    ):
        """
        検索結果画面の作成を行う
        """

        blocks = []
        blocks.append(
            {
                "type": "image",
                "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
                "alt_text": "",
            },
        )
        for book in book_results:
            blocks.extend(generate_book_block(book))

        view = {
            "type": "modal",
            "callback_id": "view_book_search",
            "private_metadata": private_metadata,
            "title": {
                "type": "plain_text",
                "text": "書籍の検索結果",
                "emoji": True,
            },
            "close": {"type": "plain_text", "text": "戻る", "emoji": True},
            "submit": {"type": "plain_text", "text": "決定", "emoji": True},
            "blocks": blocks,
        }

        return view

    def generate_book_block(book: SearchedBook):
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
                        "action_id": "google_books_buttons-action",
                    },
                ],
            },
        ]

        return block

    @app.action("select_buttons-action")
    def handle_book_selected(ack, body, _, client):
        """
        検索結果画面で選択ボタンを選択した時に行う処理
        """

        private_metadata = body["view"]["private_metadata"]

        # private_metadataに格納していた情報を復元する
        search_result: list = json.loads(private_metadata)

        # private_metadataに選択情報が入っている場合は取り除く
        search_result = [x for x in search_result if x.get("isbn", None) is not None]

        isbn = body["actions"][0]["value"]
        title = [x for x in search_result if x["isbn"] == isbn][0]["title"]

        # private_metadataに選択情報を追加する
        selected_item = {"selected_title": title, "selected_isbn": isbn}
        search_result.append(selected_item)

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

        # Blocksで渡ってくるimageには余計なパラメータが付与されているため一旦削除して付け直す
        new_blocks = [x for x in new_blocks if x["type"] != "image"]
        new_blocks.insert(
            0,
            {
                "type": "image",
                "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
                "alt_text": "",
            },
        )

        new_view = {
            "type": "modal",
            "callback_id": "view_book_search",
            "private_metadata": json.dumps(search_result),
            "title": {
                "type": "plain_text",
                "text": "書籍の検索結果",
                "emoji": True,
            },
            "close": {"type": "plain_text", "text": "戻る", "emoji": True},
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
            "type": "actions",  # pylint: disable=duplicate-code
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
                    "action_id": "google_books_buttons-action",
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
                    "action_id": "google_books_buttons-action",
                },
            ],
        }

    @app.action("google_books_buttons-action")
    def handle_google_books_selected(ack, body, _, logger):
        """
        検索結果画面でGoogle Booksで見るボタンを押した時に行う処理

        何か処理する必要はないがackを返さないとエラーが発生するのでackのみ返す
        """
        ack()
        logger.info(body)

    # view_submission リクエストを処理
    @app.view("view_book_search")
    def handle_submission(ack, body, _, __):
        """
        検索結果画面で決定ボタンを押した時に行う処理
        """

        # 通常のボタン押下状態はactionsには入ってこないためprivate_metadataで伝達する
        # private_metadataに格納していたCacheを文字列から復元する
        cache_list = body["view"]["private_metadata"]
        items: list = json.loads(cache_list)

        books = [x for x in items if x.get("selected_title", None) is not None]

        if len(books) == 0:
            ack(
                response_action="push",
                view={
                    "type": "modal",
                    "title": {"type": "plain_text", "text": "エラー", "emoji": True},
                    "close": {"type": "plain_text", "text": "OK", "emoji": True},
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "plain_text",
                                "text": "本が選択されていません",
                                "emoji": True,
                            },
                        },
                    ],
                },
            )
            return

        blocks = body["view"]["blocks"]

        # 選択された本のbook_sectionを、ISBNをもとに取得する (ハック的な対処なので注意)
        selected_book_section = None

        for i, block in enumerate(blocks):
            if (
                "elements" in block
                and block["elements"][0]["value"] == books[0]["selected_isbn"]
            ):
                selected_book_section = blocks[i - 1]  # iは選択された本のaction blockのindex

        if not selected_book_section:
            ack(
                response_action="push",
                view={
                    "type": "modal",
                    "title": {"type": "plain_text", "text": "エラー", "emoji": True},
                    "close": {"type": "plain_text", "text": "OK", "emoji": True},
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "plain_text",
                                "text": "本のデータ取得でエラーが発生しました",
                                "emoji": True,
                            },
                        },
                    ],
                },
            )
            return

        ack(
            response_action="push",
            view=generate_review_input_modal_view(selected_book_section),
        )
