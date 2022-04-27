from typing import Optional, Tuple
from bee_slack_app.service.book_search import search_book_by_title, search_book_by_isbn
from bee_slack_app.view_controller.review import generate_review_input_modal_view


def book_search_controller(app):
    @app.action("book_search")
    def open_book_search(ack, body, client):
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

                print(book_results[0])

                new_view = generate_search_result_model_view(options=search_list)
                client.views_push(trigger_id=body["trigger_id"], view=new_view)

    @app.action("radio_buttons-action")
    def handle_book_selected(ack, body, new_view, client, logger):

        print(f"view = {new_view}")
        print(f"body = {body}")

        view_id = body["container"]["view_id"]
        print(f"view_id = {view_id}")

        book_title = body["actions"][0]["selected_option"]["text"]["text"]
        isbn = body["actions"][0]["selected_option"]["value"]
        options = body["view"]["blocks"][0]["accessory"]["options"]
        print(f"book title = {book_title}")
        print(f"isbn = {isbn}")
        print(f"options = {options}")

        new_view = generate_search_result_model_view(
            options=options, selected_isbn=isbn
        )
        print(f"new_view = {new_view}")

        logger.info(body)

        client.views_update(
            view_id=view_id,
            view=new_view,
        )
        ack()

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
        ack(
            response_action="update",
            view=generate_review_input_modal_view(book_title, isbn),
        )

    def generate_search_result_model_view(options, selected_isbn=None):
        def isbn_to_urls(isbn: Optional[str]) -> Tuple[str, str]:
            dummy_url = "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg"
            if isbn is None:
                return dummy_url, dummy_url

            book = search_book_by_isbn(isbn)

            print(f"searched book = {book}")
            image_url = (
                book["image_url"]
                if book is not None and book["image_url"] is not None
                else dummy_url
            )
            google_books_url = book["google_books_url"]
            return google_books_url, image_url

        google_books_url, image_url = isbn_to_urls(selected_isbn)
        print(f"image_url = {image_url}")

        view = {
            "type": "modal",
            # ビューの識別子
            "callback_id": "view_book_search",
            "title": {
                "type": "plain_text",
                "text": "本の検索結果",
                "emoji": True,
            },
            "submit": {"type": "plain_text", "text": "選択", "emoji": True},
            "blocks": [
                {
                    "type": "section",
                    "block_id": "book_select",
                    "text": {
                        "type": "plain_text",
                        "text": "選択してください",
                    },
                    "accessory": {
                        "type": "radio_buttons",
                        "options": options,
                        "action_id": "radio_buttons-action",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{google_books_url}|Jump to Google Books>",
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": image_url,
                        "alt_text": "",
                    },
                },
            ],
        }

        return view
