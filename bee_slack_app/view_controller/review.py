import json
import os
from typing import Any, TypedDict

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.model.user import User
from bee_slack_app.service import (
    book_search_service,
    review_service,
    user_action_service,
    user_service,
)
from bee_slack_app.view.common import simple_modal
from bee_slack_app.view.post_review import (
    notify_review_post_message_blocks,
    search_book_to_review_modal,
)
from bee_slack_app.view.read_review import (
    BookOfReview,
    review_detail_modal,
    review_modal,
    review_of_user_modal,
)
from bee_slack_app.view.user import user_department_dict

BOOK_NUMBER_PER_PAGE = 19


def review_controller(app):  # pylint: disable=too-many-statements
    @app.action("read_review_of_book_action")
    def read_review_of_book_action(ack, body, client, action):
        """
        本のレビューモーダルを開く
        """
        ack()

        user_id = body["user"]["id"]

        isbn = action["value"]

        reviews = review_service.get_reviews_by_isbn(isbn=isbn)

        user_action_service.record_user_action(
            user_id=user_id,
            action_name="read_review_of_book_action",
            payload={"isbn": isbn, "reviews": reviews},
        )

        if not reviews:
            client.views_open(
                trigger_id=body["trigger_id"],
                view=simple_modal(title="エラー", text="レビュー取得でエラーが発生しました"),
            )
            return

        reviews = _make_review_contents_list_comment_short(reviews)

        # 全てのレビューで対象の本は同じなので、最初の一つを取り出す
        book: BookOfReview = {
            "isbn": reviews[0]["isbn"],
            "author": reviews[0]["book_author"],
            "title": reviews[0]["book_title"],
            "url": reviews[0]["book_url"],
            "image_url": reviews[0]["book_image_url"],
        }

        client.views_open(
            trigger_id=body["trigger_id"],
            view=review_modal(callback_id="review_modal", book=book, reviews=reviews),
        )

    @app.action("read_review_of_user_action")
    def read_review_of_user_action(ack, body, client, action):
        """
        選択したユーザのレビューリストを開く
        """
        ack()

        user_id = body["user"]["id"]
        user_id_of_review = action["value"]

        review_items = review_service.get_next_reviews_by_user_id(
            user_id=user_id_of_review, limit=BOOK_NUMBER_PER_PAGE, keys=[]
        )

        reviews = []
        if review_items:
            reviews = review_items.get("items")
            reviews = _make_review_contents_list_comment_short(reviews)

            reviews_param = {
                "reviews": reviews,
                "show_move_to_back": False,
                "show_move_to_next": review_items.get("has_next"),
            }
            # メタデータに変換する
            metadata_str = _PrivateMetadataConvertor.to_private_metadata(
                keys=review_items.get("keys"),
                user_id_of_review=user_id_of_review,
            )

        user_action_service.record_user_action(
            user_id=user_id,
            action_name="read_review_of_user_action",
            payload={"user_id_of_review": user_id_of_review, "reviews": reviews},
        )

        if not reviews:
            client.views_push(
                trigger_id=body["trigger_id"],
                view=simple_modal(title="エラー", text="レビュー取得でエラーが発生しました"),
            )
            return

        client.views_push(
            trigger_id=body["trigger_id"],
            view=review_of_user_modal(
                callback_id="review_of_user_modal",
                reviews_param=reviews_param,
                private_metadata=metadata_str,
            ),
        )

    @app.action("review_move_to_next_action")
    def review_move_to_next_action(
        ack, client, body
    ):  # pylint: disable=too-many-locals
        """
        レビューリストで「次へ」を押下されたときの処理
        """
        ack()

        user_id = body["user"]["id"]

        # メタデータから取り出す
        private_metadata = body["view"]["private_metadata"]
        metadata_dict = _PrivateMetadataConvertor.to_dict(
            private_metadata=private_metadata
        )
        user_id_of_review = metadata_dict["user_id_of_review"]

        reviews_param = None
        metadata_str = ""

        review_items = review_service.get_next_reviews_by_user_id(
            user_id=user_id_of_review,
            limit=BOOK_NUMBER_PER_PAGE,
            keys=metadata_dict["keys"],
        )

        if review_items:
            reviews = review_items.get("items")
            reviews = _make_review_contents_list_comment_short(reviews)

            reviews_param = {
                "reviews": review_items.get("items"),
                "show_move_to_back": True,
                "show_move_to_next": review_items.get("has_next"),
            }
            # メタデータに変換する
            metadata_str = _PrivateMetadataConvertor.to_private_metadata(
                keys=review_items.get("keys"),
                user_id_of_review=user_id_of_review,
            )

        user_action_service.record_user_action(
            user_id=user_id,
            action_name="read_review_of_user_action",
            payload={"user_id_of_review": user_id_of_review, "reviews": reviews},
        )

        client.views_update(
            view_id=body.get("view").get("id"),
            view=review_of_user_modal(
                callback_id="review_of_user_modal",
                reviews_param=reviews_param,
                private_metadata=metadata_str,
            ),
        )

    @app.action("review_move_to_back_action")
    def review_move_to_back_action(
        ack, client, body
    ):  # pylint: disable=too-many-locals
        """
        レビューリストで「前へ」を押下されたときの処理
        """
        ack()

        user_id = body["user"]["id"]

        # メタデータから取り出す
        private_metadata = body["view"]["private_metadata"]
        metadata_dict = _PrivateMetadataConvertor.to_dict(
            private_metadata=private_metadata
        )
        user_id_of_review = metadata_dict["user_id_of_review"]

        reviews_param = None
        metadata_str = ""

        review_items = review_service.get_before_reviews_by_user_id(
            user_id=user_id_of_review,
            limit=BOOK_NUMBER_PER_PAGE,
            keys=metadata_dict["keys"],
        )
        if review_items:
            reviews = review_items.get("items")
            reviews = _make_review_contents_list_comment_short(reviews)

            reviews_param = {
                "reviews": review_items.get("items"),
                "show_move_to_back": not review_items.get("is_move_to_first"),
                "show_move_to_next": True,
            }
            # メタデータに変換する
            metadata_str = _PrivateMetadataConvertor.to_private_metadata(
                keys=review_items.get("keys"),
                user_id_of_review=user_id_of_review,
            )

        user_action_service.record_user_action(
            user_id=user_id,
            action_name="read_review_of_user_action",
            payload={"user_id_of_review": user_id_of_review, "reviews": reviews},
        )

        client.views_update(
            view_id=body.get("view").get("id"),
            view=review_of_user_modal(
                callback_id="review_of_user_modal",
                reviews_param=reviews_param,
                private_metadata=metadata_str,
            ),
        )

    @app.action("post_review_action")
    def open_book_search_modal(ack, body, client):
        """
        本の検索モーダルを開く
        """
        ack()

        user_id = body["user"]["id"]

        if not user_service.get_user(user_id):
            user_action_service.record_user_action(
                user_id=user_id,
                action_name="post_review_action",
                status="no_user_profile_error",
            )

            client.views_open(
                trigger_id=body["trigger_id"],
                view=simple_modal(
                    title="プロフィールを入力してください", text="レビューを投稿するには、プロフィールの入力が必要です :bow:"
                ),
            )
            return

        user_action_service.record_user_action(
            user_id=user_id,
            action_name="post_review_action",
        )

        client.views_open(
            trigger_id=body["trigger_id"],
            view_id=body["view"]["id"],
            hash=body["view"]["hash"],
            view=search_book_to_review_modal(callback_id="book_search_modal"),
        )

    @app.view("post_review_modal")
    def handle_submission(
        ack, body, _, view, client
    ):  # pylint: disable=too-many-locals

        # ハック的な対処なので注意
        # "*<本のタイトル>*\n<本の著者>\nISBN-<本のISBN>"のような文字列からタイトルやISBNを抜き出す
        book_title_author_isbn = view["blocks"][1]["text"]["text"]
        isbn = book_title_author_isbn.split("-")[-1]

        # ISBNが取れたらもう一度Google Books APIから本の情報を取り直す
        # Descriptionを追加する関係で表示画面情報からだけでは足りなくなり
        # APIから再取得することにする
        book_info = book_search_service.search_book_by_isbn(isbn)

        # 必ず取得できるのでelse側の考慮は不要
        # ただしImage URLだけは例外
        # TODO: 暫定で適当な画像をデフォルトに設定、S3に画像を置くようになったら自前の画像に差し替える
        dummy_url = "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg"

        if book_info is not None:
            book_title = book_info["title"]
            author = ",".join(book_info["authors"])
            image_url = (
                book_info["image_url"]
                if book_info["image_url"] is not None
                else dummy_url
            )
            book_url = book_info["google_books_url"]
            book_description = book_info["description"]

        score_for_me = view["state"]["values"]["input_score_for_me"][
            "score_for_me_action"
        ]["selected_option"]["value"]
        score_for_others = view["state"]["values"]["input_score_for_others"][
            "score_for_others_action"
        ]["selected_option"]["value"]
        review_comment = view["state"]["values"]["input_comment"]["comment_action"][
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
            "book_url": book_url,
            "book_description": book_description,
        }

        review = review_service.post_review(review_contents)

        notify = not bool(
            view["state"]["values"]["disable_notify_review_post_block"][
                "disable_notify_review_post_action"
            ]["selected_options"]
        )

        user_action_service.record_user_action(
            user_id=user_id,
            action_name="post_review_modal",
            payload={"review": review_contents, "notify": notify},
        )

        if notify:
            user = user_service.get_user(review["user_id"])
            review["user_name"] = (
                _make_detailed_user_name(user) if user else review["user_id"]
            )

            blocks = notify_review_post_message_blocks(review)
            client.chat_postMessage(
                channel=os.environ["NOTIFY_POST_REVIEW_CHANNEL"],
                blocks=blocks,
                text=f"{review['user_name']}さんがレビューを投稿しました",
            )

    def _make_detailed_user_name(user: User) -> str:
        """
        ユーザー名を部署名付きのものに変換する
        """
        return f'{user["user_name"]}  ({user_department_dict[user["department"]]})'

    @app.action("open_review_detail_modal_action")
    def open_review_detail_modal(ack, body, client, action):
        ack()

        user_id, isbn = action["value"].split(":")

        review = review_service.get_review(user_id=user_id, isbn=isbn)

        if not review:
            user_action_service.record_user_action(
                user_id=body["user"]["id"],
                action_name="open_review_detail_modal_action",
                status="fetch_review_data_error",
            )

            client.views_push(
                trigger_id=body["trigger_id"],
                view=simple_modal(title="エラー", text="レビューの取得でエラーが発生しました"),
            )
            return

        user_action_service.record_user_action(
            user_id=body["user"]["id"],
            action_name="open_review_detail_modal_action",
            payload={"review": review},
        )

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


class _PrivateMetadataConvertor:
    class _MetadataDict(TypedDict):
        keys: Any
        user_id_of_review: Any

    @staticmethod
    # メタデータへの変換
    def to_private_metadata(*, keys: Any, user_id_of_review: str) -> str:
        return json.dumps({"keys": keys, "user_id_of_review": user_id_of_review})

    @staticmethod
    # メタデータから取り出し
    def to_dict(*, private_metadata: str) -> _MetadataDict:
        return json.loads(private_metadata)
