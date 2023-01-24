import json
from typing import Optional, TypedDict

from slack_bolt import App

from bee_slack_app.model import Review, ReviewPagination, User
from bee_slack_app.service import review_service, user_action_service, user_service
from bee_slack_app.view import review_of_user_modal, simple_modal, user_profile_modal

BOOK_NUMBER_PER_PAGE = 20


def user_controller(app: App) -> None:
    @app.action("user_info_action")
    def open_user_info(ack, body, client):
        ack()
        user_id = body["user"]["id"]

        # ユーザー情報の取得
        user: Optional[User] = user_service.get_user(user_id)

        # slackアカウントから名前（Display Name）Display Nameを取得する
        # display_nameを設定していない場合は、設定必須のreal_nameをユーザ名とすることで、対応する
        user_info = client.users_info(user=user_id)
        user_name = (
            user_info["user"]["profile"]["display_name"]
            or user_info["user"]["profile"]["real_name"]
        )

        post_review_count = str(user["post_review_count"]) if user else "0"

        private_metadata = _PrivateMetadataConvertor.to_private_metadata(
            post_review_count=post_review_count
        )

        modal_view = user_profile_modal(
            callback_id="user_profile_modal",
            private_metadata=private_metadata,
            user_name=user_name,
            user=user,
        )

        user_action_service.record_user_action(
            user_id=user_id,
            action_name="user_info_action",
            payload={"user_info": user_info},
        )

        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )

    @app.view("user_profile_modal")
    def handle_submission(ack, body, _, view):

        user_name = view["blocks"][0]["text"]["text"]

        department = view["state"]["values"]["input_department"]["department_action"][
            "selected_option"
        ]["value"]

        job_type = view["state"]["values"]["input_job_type"]["job_type_action"][
            "selected_option"
        ]["value"]

        age_range = view["state"]["values"]["input_age_range"]["age_range_action"][
            "selected_option"
        ]["value"]

        user_id = body["user"]["id"]

        private_metadata = body["view"]["private_metadata"]

        metadata_dict = _PrivateMetadataConvertor.to_dict(
            private_metadata=private_metadata
        )

        ack()

        user: User = {
            "user_id": user_id,
            "user_name": user_name,
            "department": department,
            "job_type": job_type,
            "age_range": age_range,
            "updated_at": None,
            "post_review_count": int(metadata_dict["post_review_count"]),
        }

        user_service.add_user(user)

        user_action_service.record_user_action(
            user_id=user_id,
            action_name="user_profile_modal",
            payload={"user": user},
        )


def _make_review_contents_list_comment_short(
    review_contents_list: list[Review],
) -> list[Review]:
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
        post_review_count: str

    @staticmethod
    def to_private_metadata(*, post_review_count: str) -> str:
        return json.dumps({"post_review_count": post_review_count})

    @staticmethod
    def to_dict(*, private_metadata: str) -> _MetadataDict:
        return json.loads(private_metadata)
