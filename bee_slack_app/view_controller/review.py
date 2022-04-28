from bee_slack_app.model.review import ReviewContents
from bee_slack_app.service.review import get_review_all, post_review


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
            view=generate_review_input_modal_view(),
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

    @app.action("read_review")
    def open_read_modal(ack, body, client, logger):
        # コマンドのリクエストを確認
        ack()

        # レビューを全件取得する
        review_contents_list: list[ReviewContents] = get_review_all(logger)

        review_list = []

        for review_contents in review_contents_list:

            # 空はエラーになるため、ハイフンを設定
            # TODO: 本来 review_comment が None になることは想定されていない（get_review_allが返す型と不一致）なので、service側での修正が必要
            review_comment = review_contents["review_comment"]
            review_comment = (
                review_comment
                if review_comment is not None and len(review_comment) > 0
                else "-"
            )

            review_item = {
                "type": "section",
                "fields": [
                    {
                        "type": "plain_text",
                        "text": "本のタイトル",
                        "emoji": True,
                    },
                    {
                        "type": "plain_text",
                        "text": review_contents["book_title"],
                        "emoji": True,
                    },
                    {
                        "type": "plain_text",
                        "text": "ISBN",
                        "emoji": True,
                    },
                    {
                        "type": "plain_text",
                        "text": review_contents["isbn"],
                        "emoji": True,
                    },
                    {
                        "type": "plain_text",
                        "text": "自分にとっての評価",
                        "emoji": True,
                    },
                    {
                        "type": "plain_text",
                        "text": str(review_contents["score_for_me"]),
                        "emoji": True,
                    },
                    {
                        "type": "plain_text",
                        "text": "他の人へのおすすめ度",
                        "emoji": True,
                    },
                    {
                        "type": "plain_text",
                        "text": str(review_contents["score_for_others"]),
                        "emoji": True,
                    },
                    {
                        "type": "plain_text",
                        "text": "レビューコメント",
                        "emoji": True,
                    },
                    {
                        "type": "plain_text",
                        "text": review_comment,
                        "emoji": True,
                    },
                ],
            }

            review_list.append(review_item)
            review_list.append({"type": "divider"})

        client.views_open(
            trigger_id=body["trigger_id"],
            view_id=body["view"]["id"],
            hash=body["view"]["hash"],
            # ビューのペイロード
            view={
                "type": "modal",
                # ビューの識別子
                "callback_id": "view_1",
                "title": {"type": "plain_text", "text": "Bee"},
                "blocks": review_list,
            },
        )


def generate_review_input_modal_view(book_title="", isbn=""):
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
                "label": {"type": "plain_text", "text": "ISBN"},
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
                    "type": "static_select",
                    "action_id": "action_id_score_for_me",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "選択してください",
                        "emoji": True,
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
                "label": {"type": "plain_text", "text": "他の人へのおすすめ度"},
                "element": {
                    "type": "static_select",
                    "action_id": "action_id_score_for_others",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "選択してください",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "value": "5",
                            "text": {"type": "plain_text", "text": "とてもおすすめ"},
                        },
                        {
                            "value": "4",
                            "text": {"type": "plain_text", "text": "おすすめ"},
                        },
                        {
                            "value": "3",
                            "text": {"type": "plain_text", "text": "普通"},
                        },
                        {
                            "value": "2",
                            "text": {"type": "plain_text", "text": "おすすめしない"},
                        },
                        {
                            "value": "1",
                            "text": {"type": "plain_text", "text": "絶対におすすめしない"},
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
