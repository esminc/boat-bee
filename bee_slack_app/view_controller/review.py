import json

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.service.review import get_reviews, get_reviews_before, post_review
from bee_slack_app.service.user import get_user
from bee_slack_app.utils import datetime


def review_controller(app):  # pylint: disable=too-many-statements
    review_item_limit = 10

    @app.action("post_review")
    def open_book_search_modal(ack, body, client, logger):
        """
        本の検索モーダルを開く
        """
        # コマンドのリクエストを確認
        ack()

        if not get_user(logger, body["user"]["id"]):
            client.views_open(
                trigger_id=body["trigger_id"],
                view={
                    "type": "modal",
                    "title": {
                        "type": "plain_text",
                        "text": "プロフィールを入力してください",
                        "emoji": True,
                    },
                    "close": {"type": "plain_text", "text": "OK", "emoji": True},
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "レビューを投稿するには、プロフィールの入力が必要です :bow:",
                            },
                        },
                    ],
                },
            )
            return

        client.views_open(
            trigger_id=body["trigger_id"],
            view_id=body["view"]["id"],
            hash=body["view"]["hash"],
            # ビューのペイロード
            view={
                "type": "modal",
                "callback_id": "book_search_modal",
                "title": {"type": "plain_text", "text": "レビューする本を検索する"},
                "submit": {"type": "plain_text", "text": "書籍の検索"},
                "blocks": [
                    {
                        "type": "input",
                        "block_id": "input_book_title",
                        "label": {"type": "plain_text", "text": "タイトル"},
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "action_id_book_title",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "本のタイトルを入力してください",
                                "emoji": True,
                            },
                        },
                    },
                    {
                        "type": "image",
                        "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
                        "alt_text": "",
                    },
                ],
            },
        )

    # view_submission リクエストを処理
    @app.view("view_1")
    def handle_submission(ack, body, _, view, logger):

        # ハック的な対処なので注意
        # "*<本のタイトル>*\n<本の著者>\nISBN-<本のISBN>"のような文字列からタイトルやISBNを抜き出す
        book_title_author_isbn = view["blocks"][1]["text"]["text"]
        book_title = book_title_author_isbn.split("*")[1]
        isbn = book_title_author_isbn.split("-")[-1]
        author = book_title_author_isbn.split("*")[2].split("-")[-2][:-5][1:]
        image_url = view["blocks"][1]["accessory"]["image_url"]

        score_for_me = view["state"]["values"]["input_score_for_me"][
            "action_id_score_for_me"
        ]["selected_option"]["value"]
        score_for_others = view["state"]["values"]["input_score_for_others"][
            "action_id_score_for_others"
        ]["selected_option"]["value"]

        # `input_comment`という block_id に `action_id_comment` を持つ input ブロックがある場合
        review_comment = view["state"]["values"]["input_comment"]["action_id_comment"][
            "value"
        ]
        user_id = body["user"]["id"]
        # 入力値を検証
        errors = {}
        if review_comment is not None and len(review_comment) <= 1:
            errors["input_comment"] = "The value must be longer than 5 characters"
        if len(errors) > 0:
            ack(response_action="errors", errors=errors)
            return
        # view_submission リクエストの確認を行い、モーダルを閉じる
        # この時、最初に開いていたモーダルも含めてすべて閉じるために
        # response_action="clear" を設定する
        ack(response_action="clear")

        review_contents: ReviewContents = {
            "user_id": user_id,
            "book_title": book_title,
            "isbn": isbn,
            "score_for_me": score_for_me,
            "score_for_others": score_for_others,
            "review_comment": review_comment,
            "updated_at": None,
            "book_image_url": image_url,
            "book_author": author,
            "book_url": json.loads(view["private_metadata"])["url"],
        }

        post_review(logger, review_contents)

    @app.action("read_review")
    def open_read_modal(ack, body, client, logger):
        # コマンドのリクエストを確認
        ack()

        reviews = get_reviews(logger=logger, limit=review_item_limit, keys=[])

        metadata_str = ReviewPrivateMetadataConvertor.convert_to_private_metadata(
            keys=reviews["keys"]
        )

        view = generate_review_list_modal_view(
            reviews["items"],
            private_metadata=metadata_str,
            show_move_to_next=bool(reviews["keys"]),
        )

        client.views_open(
            trigger_id=body["trigger_id"],
            view=view,
        )

    @app.action("move_to_next")
    def move_to_next(ack, logger, client, body):
        ack()

        metadata_dict = ReviewPrivateMetadataConvertor.convert_to_dict(
            private_metadata=body["view"]["private_metadata"]
        )
        keys = metadata_dict["keys"]

        conditions = metadata_dict.get("conditions")

        reviews = get_reviews(
            logger=logger, limit=review_item_limit, keys=keys, conditions=conditions
        )

        metadata_str = ReviewPrivateMetadataConvertor.convert_to_private_metadata(
            keys=reviews["keys"], conditions=conditions
        )

        view = generate_review_list_modal_view(
            reviews["items"],
            private_metadata=metadata_str,
            show_move_to_back=True,
            show_move_to_next=reviews["keys"][-1] != "end",
        )

        client.views_update(
            trigger_id=body["trigger_id"],
            view_id=body["view"]["id"],
            hash=body["view"]["hash"],
            view=view,
        )

    @app.action("move_to_back")
    def move_to_back(ack, logger, client, body):
        ack()

        metadata_dict = ReviewPrivateMetadataConvertor.convert_to_dict(
            private_metadata=body["view"]["private_metadata"]
        )
        keys = metadata_dict["keys"]

        is_move_to_first = len(keys) < 3

        conditions = metadata_dict.get("conditions")

        reviews = get_reviews_before(
            logger=logger, limit=review_item_limit, keys=keys, conditions=conditions
        )

        metadata_str = ReviewPrivateMetadataConvertor.convert_to_private_metadata(
            keys=reviews["keys"], conditions=conditions
        )

        view = generate_review_list_modal_view(
            reviews["items"],
            private_metadata=metadata_str,
            show_move_to_back=not is_move_to_first,
        )

        client.views_update(
            trigger_id=body["trigger_id"],
            view_id=body["view"]["id"],
            hash=body["view"]["hash"],
            view=view,
        )

    @app.action("search_review")
    def update_review_list_view(ack, body, client, logger):
        ack()

        values_from_body = body["view"]["state"]["values"]

        scores = {}

        for label in ["score_for_me", "score_for_others"]:

            select_block = values_from_body[f"{label}_select_block"]
            selected_option = select_block[f"{label}_select_action"]["selected_option"]
            score = selected_option and selected_option.get("value")

            if score in ["1", "2", "3", "4", "5"]:
                scores[label] = score

        reviews = get_reviews(
            logger=logger, conditions=scores, limit=review_item_limit, keys=[]
        )

        private_metadata = ReviewPrivateMetadataConvertor.convert_to_private_metadata(
            keys=reviews["keys"], conditions=scores
        )

        view = generate_review_list_modal_view(
            reviews["items"],
            private_metadata=private_metadata,
            show_move_to_next=bool(reviews["keys"]),
        )

        client.views_update(
            trigger_id=body["trigger_id"],
            view_id=body["view"]["id"],
            hash=body["view"]["hash"],
            # ビューのペイロード
            view=view,
        )

    @app.action("score_for_me_select_action")
    def score_for_me_select_action(ack):
        # 何もしない
        ack()

    @app.action("score_for_others_select_action")
    def score_for_others_select_action(ack):
        # 何もしない
        ack()


class ReviewPrivateMetadataConvertor:
    @staticmethod
    def convert_to_private_metadata(*, keys, conditions=None):

        metadata = {"keys": keys}

        if conditions:
            metadata["conditions"] = conditions

        return json.dumps(metadata)

    @staticmethod
    def convert_to_dict(*, private_metadata):

        return json.loads(private_metadata)


def generate_review_input_modal_view(book_section, url: str):
    private_metadata = json.dumps({"url": url})

    view = {
        "type": "modal",
        # ビューの識別子
        "callback_id": "view_1",
        "private_metadata": private_metadata,
        "title": {"type": "plain_text", "text": "Bee"},
        "submit": {"type": "plain_text", "text": "送信"},
        "close": {"type": "plain_text", "text": "戻る", "emoji": True},
        "blocks": [
            {
                "type": "image",
                "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
                "alt_text": "",
            },
            book_section,
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
                "label": {"type": "plain_text", "text": "永和社員へのおすすめ度"},
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


def generate_review_list_modal_view(
    review_contents_list: list[ReviewContents],
    private_metadata=None,
    show_move_to_back=False,
    show_move_to_next=True,
):
    review_list = []

    for review_contents in review_contents_list:

        # 空はエラーになるため、ハイフンを設定
        # TODO: 本来 review_comment が None になることは想定されていない（get_reviewsが返す型と不一致）なので、service側での修正が必要
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
                    "text": "永和社員へのおすすめ度",
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

        update_datetime = (
            datetime.parse(review_contents["updated_at"])
            if review_contents["updated_at"]
            else "-"
        )

        review_post_item = {
            "type": "section",
            "fields": [
                {
                    "type": "plain_text",
                    "text": "投稿者",
                    "emoji": True,
                },
                {
                    "type": "plain_text",
                    "text": review_contents["user_id"],
                    "emoji": True,
                },
                {
                    "type": "plain_text",
                    "text": "投稿日時",
                    "emoji": True,
                },
                {
                    "type": "plain_text",
                    "text": update_datetime,
                    "emoji": True,
                },
            ],
        }
        review_list.append(review_post_item)
        review_list.append({"type": "divider"})

    move_buttons = {
        "type": "actions",
        "elements": [],
    }

    if show_move_to_back:
        move_buttons["elements"] = [
            {  # type: ignore
                "type": "button",
                "text": {"type": "plain_text", "text": "前へ"},
                "action_id": "move_to_back",
            }
        ]

    if show_move_to_next:
        move_buttons["elements"] = move_buttons["elements"] + [  # type: ignore
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "次へ"},
                "action_id": "move_to_next",
            }
        ]

    return {
        "private_metadata": private_metadata or "[]",
        "type": "modal",
        "callback_id": "update_review_list_view",
        "title": {"type": "plain_text", "text": "Bee"},
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": "*検索条件*"}},
            {
                "block_id": "score_for_me_select_block",
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "自分にとっての評価",
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "未指定",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "value": "0",
                            "text": {"type": "plain_text", "text": "未指定"},
                        },
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
                    "action_id": "score_for_me_select_action",
                },
            },
            {
                "block_id": "score_for_others_select_block",
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "永和社員へのおすすめ度",
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "未指定",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "value": "0",
                            "text": {"type": "plain_text", "text": "未指定"},
                        },
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
                    "action_id": "score_for_others_select_action",
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "検索"},
                        "action_id": "search_review",
                    },
                ],
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*検索結果*"}},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"{len(review_contents_list)}件"},
            },
            {"type": "divider"},
        ]
        + review_list  # type: ignore
        + [move_buttons],  # type: ignore
    }
