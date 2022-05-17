import json

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.service.review import get_reviews, get_reviews_before, post_review
from bee_slack_app.service.user import get_user
from bee_slack_app.view.common import simple_modal
from bee_slack_app.view.post_review import search_book_to_review_modal
from bee_slack_app.view.read_review import review_list_modal


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
    @app.view("post_review_modal")
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

        view = review_list_modal(
            callback_id="post_review_modal",
            search_button_action_id="search_review",
            review_contents_list=reviews["items"],
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

        view = review_list_modal(
            callback_id="post_review_modal",
            search_button_action_id="search_review",
            review_contents_list=reviews["items"],
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

        view = review_list_modal(
            callback_id="post_review_modal",
            search_button_action_id="search_review",
            review_contents_list=reviews["items"],
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

        view = review_list_modal(
            callback_id="post_review_modal",
            search_button_action_id="search_review",
            review_contents_list=reviews["items"],
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
