from bee_slack_app.service.book_search import search_book_by_title
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

            search_list = []

            for book_result in book_results:
                search_item = {
                    "value": book_result["isbn"],
                    "text": {
                        "type": "plain_text",
                        "text": book_result["title"],
                        "emoji": True,
                    },
                }
                search_list.append(search_item)

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
                            "label": {
                                "type": "plain_text",
                                "text": "選択してください",
                                "emoji": True,
                            },
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
        ack(
            response_action="update",
            view=generate_review_input_modal_view(book_title, isbn),
        )
