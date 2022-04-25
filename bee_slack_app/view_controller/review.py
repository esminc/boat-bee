from bee_slack_app.model.review import ReviewContents
from bee_slack_app.service.review import post_review


def review_controller(app):
    @app.action("post_review")
    def open_modal(ack, body, client):
        # コマンドのリクエストを確認
        ack()
        client.views_open(
            trigger_id=body["trigger_id"],
            view_id=body["view"]["id"],
            hash=body["view"]["hash"],
            # ビューのペイロード
            view=open_new_modal(),
        )

    # view_submission リクエストを処理
    @app.view("view_1")
    def handle_submission(ack, body, _, view, logger):
        print("ビューからのイベント")

        book_title = view["state"]["values"]["input_book_title"][
            "action_id_book_title"
        ]["value"]
        print(f"Book title= {book_title}")
        isbn = view["state"]["values"]["input_isbn"]["action_id_isbn"]["value"]
        print(f"ISBN code= {isbn}")

        score_for_me = view["state"]["values"]["input_score_for_me"][
            "action_id_score_for_me"
        ]["selected_option"]["value"]
        print(f"Score for me= {score_for_me}")
        score_for_others = view["state"]["values"]["input_score_for_others"][
            "action_id_score_for_others"
        ]["selected_option"]["value"]
        print(f"Score for others= {score_for_others}")

        # `input_comment`という block_id に `action_id_comment` を持つ input ブロックがある場合
        review_comment = view["state"]["values"]["input_comment"]["action_id_comment"][
            "value"
        ]
        print(f"Review comment = {review_comment}")

        user_id = body["user"]["id"]
        print("user_id:", user_id)
        # 入力値を検証
        errors = {}
        if review_comment is not None and len(review_comment) <= 1:
            errors["input_comment"] = "The value must be longer than 5 characters"
        if len(errors) > 0:
            ack(response_action="errors", errors=errors)
            return
        # view_submission リクエストの確認を行い、モーダルを閉じる
        ack()

        review_contents: ReviewContents = {
            "user_id": user_id,
            "book_title": book_title,
            "isbn": isbn,
            "score_for_me": score_for_me,
            "score_for_others": score_for_others,
            "review_comment": review_comment,
        }

        post_review(logger, review_contents)


def open_new_modal(book_title="", isbn=""):
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

    return view
