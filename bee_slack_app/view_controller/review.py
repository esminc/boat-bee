import json
import os

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.service.review import (
    get_review,
    get_reviews,
    get_reviews_before,
    post_review,
)
from bee_slack_app.service.user import get_user
from bee_slack_app.view.common import simple_modal
from bee_slack_app.view.post_review import (
    notify_review_post_message_blocks,
    search_book_to_review_modal,
)
from bee_slack_app.view.read_review import review_detail_modal, review_list_modal


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
                view=simple_modal(
                    title="プロフィールを入力してください", text="レビューを投稿するには、プロフィールの入力が必要です :bow:"
                ),
            )
            return

        client.views_open(
            trigger_id=body["trigger_id"],
            view_id=body["view"]["id"],
            hash=body["view"]["hash"],
            # ビューのペイロード
            view=search_book_to_review_modal(callback_id="book_search_modal"),
        )

    # view_submission リクエストを処理
    @app.view("view_1")
    def handle_submission(
        ack, body, _, view, logger, client
    ):  # pylint: disable=too-many-locals

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

        review = post_review(logger, review_contents)

        notify = not bool(
            view["state"]["values"]["disable_notify_review_post_block"][
                "disable_notify_review_post_action"
            ]["selected_options"]
        )

        if notify:
            user = get_user(logger, review["user_id"])
            review["user_name"] = user["user_name"] if user else review["user_id"]

            blocks = notify_review_post_message_blocks(review)
            client.chat_postMessage(
                channel=os.environ["NOTIFY_POST_REVIEW_CHANNEL"], blocks=blocks
            )

    @app.action("read_review")
    def open_read_modal(ack, body, client, logger):
        # コマンドのリクエストを確認
        ack()

        reviews = get_reviews(logger=logger, limit=review_item_limit, keys=[])

        metadata_str = ReviewPrivateMetadataConvertor.convert_to_private_metadata(
            keys=reviews["keys"]
        )

        review_contents_list = _make_review_contents_list_comment_short(
            reviews["items"]
        )

        view = review_list_modal(
            callback_id="view_1",
            search_button_action_id="search_review",
            review_contents_list=review_contents_list,
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

        review_contents_list = _make_review_contents_list_comment_short(
            reviews["items"]
        )

        view = review_list_modal(
            callback_id="view_1",
            search_button_action_id="search_review",
            review_contents_list=review_contents_list,
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

        review_contents_list = _make_review_contents_list_comment_short(
            reviews["items"]
        )

        view = review_list_modal(
            callback_id="view_1",
            search_button_action_id="search_review",
            review_contents_list=review_contents_list,
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

        review_contents_list = _make_review_contents_list_comment_short(
            reviews["items"]
        )

        view = review_list_modal(
            callback_id="view_1",
            search_button_action_id="search_review",
            review_contents_list=review_contents_list,
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

    @app.action("open_review_detail_modal_action")
    def open_review_detail_modal(ack, body, client, logger, action):
        ack()

        user_id, isbn = action["value"].split(":")

        review = get_review(logger=logger, user_id=user_id, isbn=isbn)

        if not review:
            client.views_push(
                trigger_id=body["trigger_id"],
                view=simple_modal(title="エラー", text="レビューの取得でエラーが発生しました"),
            )
            return

        client.views_push(
            trigger_id=body["trigger_id"], view=review_detail_modal(review)
        )


def _make_review_contents_list_comment_short(
    review_contents_list: list[ReviewContents],
) -> list[ReviewContents]:
    """
    レビューのコメントを、一覧表示用に短くする
    """
    comment_len = 20

    for review_contents in review_contents_list:
        review_comment = review_contents["review_comment"]
        if review_comment:
            review_contents["review_comment"] = (
                review_comment[0:comment_len] + "..."
                if len(review_comment) > comment_len
                else review_comment
            )
        else:
            review_contents["review_comment"] = "-"

    return review_contents_list


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
