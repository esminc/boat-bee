import json
from pprint import pprint
from typing import List, Optional, Tuple

from bee_slack_app.service.book_search import search_book_by_isbn, search_book_by_title
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
                search_list = []
                cache_list = []

                for book_result in book_results:
                    title = book_result["title"]
                    search_item = {
                        "value": book_result["isbn"],
                        "text": {
                            "type": "mrkdwn",
                            "text": title,
                        },
                    }
                    search_list.append(search_item)

                    # ラジオボタン選択時に書籍のデータを再利用するため情報を保持しておく
                    # とりあえずはISBNからURLを取得できれば良い
                    # private_metadataに格納できる情報が3000文字なので最小限にする
                    cache_item = {
                        "isbn": book_result["isbn"],
                        "image_url": book_result["image_url"],
                        "google_books_url": book_result["google_books_url"],
                    }
                    cache_list.append(cache_item)

                # private_metadataに格納するためにCacheを文字列に変換する
                cache_list_str = json.dumps(cache_list)

                new_view = generate_search_result_model_view(
                    options=book_results, cached_search_result=cache_list_str
                )
                client.views_push(trigger_id=body["trigger_id"], view=new_view)

    def generate_search_result_model_view(
        options,
        selected_isbn: Optional[str] = None,
        cached_search_result: Optional[str] = None,
    ):
        """
        検索結果画面の作成を行う

        ISBNが与えられた場合はGoogle BooksへのURLと画像リンクを更新する
        """
        # TODO: 暫定で適当な画像をデフォルトに設定、S3に画像を置くようになったら自前の画像に差し替える
        dummy_url = "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg"

        def isbn_to_url_by_api(isbn: Optional[str]) -> Tuple[str, str]:
            """
            APIを用いてISBNからURLを取得する

            Cacheから取得できない場合にはこちらを使う
            """
            if isbn is None:
                return dummy_url, dummy_url

            book = search_book_by_isbn(isbn)

            image_url = (
                book["image_url"]
                if book is not None and book["image_url"] is not None
                else dummy_url
            )
            google_books_url = (
                book["google_books_url"]
                if book is not None and book["google_books_url"] is not None
                else dummy_url
            )

            return google_books_url, image_url

        def isbn_to_url_by_cache(
            isbn: Optional[str], search_result: List[dict[str, str]]
        ) -> Tuple[Optional[str], Optional[str]]:
            """
            Cacheを用いてISBNからURLを取得する
            """
            if isbn is None:
                return dummy_url, dummy_url

            books = [x for x in search_result if x["isbn"] == isbn]
            if len(books) == 0:
                return None, None
            book = books[0]

            image_url = (
                book.get("image_url", dummy_url)
                if book["image_url"] is not None
                else dummy_url
            )
            google_books_url = (
                book.get("google_books_url", dummy_url)
                if book["google_books_url"] is not None
                else dummy_url
            )

            return google_books_url, image_url

        def isbn_to_url(
            isbn: Optional[str], cached_search_result: Optional[str]
        ) -> Tuple[str, str]:

            # Cacheが与えられない場合はAPIを使って取得する
            if cached_search_result is None:
                return isbn_to_url_by_api(isbn)

            # private_metadataに格納していたCacheを文字列から復元する
            search_resut = json.loads(cached_search_result)

            google_books_url, image_url = isbn_to_url_by_cache(isbn, search_resut)

            # Cacheから取得できない場合はAPIを使って取得する
            if google_books_url is None or image_url is None:
                return isbn_to_url_by_api(isbn)

            return google_books_url, image_url

        google_books_url, image_url = isbn_to_url(selected_isbn, cached_search_result)

        blocks = []

        for book in options:
            # print(book)

            blocks.extend(generate_searched_book(book))

        view = {
            "type": "modal",
            # ビューの識別子
            "callback_id": "view_book_search",
            "private_metadata": cached_search_result,
            "title": {
                "type": "plain_text",
                "text": "本の検索結果",
                "emoji": True,
            },
            "submit": {"type": "plain_text", "text": "選択", "emoji": True},
            "blocks": blocks,
        }

        return view

    def generate_searched_book(book):
        # TODO: 暫定で適当な画像をデフォルトに設定、S3に画像を置くようになったら自前の画像に差し替える
        dummy_url = "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg"

        # print(book)

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
    def handle_book_selected(ack, body, _, client, logger):
        """
        検索結果画面でボタンを選択した時に行う処理
        """

        actions = body["actions"]
        # pprint(f"actions = {actions}")

        isbn = body["actions"][0]["value"]
        # print(f"isbn = {isbn}")

        blocks = body["view"]["blocks"]

        pprint(f"blocks = {blocks}")

        new_blocks = [
            x
            if x["type"] != "actions"
            else selected_book(x)
            if x["elements"][0]["value"] == isbn
            else unselected_book(x)
            for x in blocks
        ]
        pprint(f"new_blocks = {new_blocks}")

        new_view = {
            "type": "modal",
            # ビューの識別子
            "callback_id": "view_book_search",
            "title": {
                "type": "plain_text",
                "text": "本の検索結果",
                "emoji": True,
            },
            # "private_metadata": ,
            "submit": {"type": "plain_text", "text": "選択", "emoji": True},
            "blocks": new_blocks,
        }
        client.views_update(
            view_id=body["container"]["view_id"],
            view=new_view,
        )
        ack()

    def selected_book(item):
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

    @app.action("radio_buttons-action")
    def handle_book_selected_(ack, body, new_view, client, logger):
        """
        検索結果画面でラジオボタンを選択した時に行う処理

        選択に応じてGoogle BooksへのURLと画像リンクを更新する
        """

        isbn = body["actions"][0]["selected_option"]["value"]
        options = body["view"]["blocks"][0]["accessory"]["options"]
        cache_list = body["view"]["private_metadata"]

        new_view = generate_search_result_model_view(
            options=options, selected_isbn=isbn, cached_search_result=cache_list
        )

        logger.info(body)

        client.views_update(
            view_id=body["container"]["view_id"],
            view=new_view,
        )
        ack()

    # view_submission リクエストを処理
    @app.view("view_book_search")
    def handle_submission(ack, _, __, view):
        """
        検索結果画面で選択ボタンを押下したときに行う処理
        """
        book_title = view["state"]["values"]["book_select"]["radio_buttons-action"][
            "selected_option"
        ]["text"]["text"]
        isbn = view["state"]["values"]["book_select"]["radio_buttons-action"][
            "selected_option"
        ]["value"]

        # view_submission リクエストの確認を行い、モーダルを閉じる
        ack(
            response_action="update",
            view=generate_review_input_modal_view(book_title, isbn),
        )
