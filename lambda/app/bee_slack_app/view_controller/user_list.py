from bee_slack_app.service.user import get_users_posted_review
from bee_slack_app.view.user_list import posted_review_user_list_modal
from bee_slack_app.view_controller.utils import respond_to_slack_within_3_seconds


def user_list_controller(app):
    def list_user_posted_review_action(ack, body, client):
        """
        レビューを投稿したユーザモーダルを開く
        """
        ack()

        users = get_users_posted_review()

        client.views_open(
            trigger_id=body["trigger_id"],
            view=posted_review_user_list_modal(callback_id="review_modal", users=users),
        )

    app.action("list_user_posted_review_action")(
        ack=respond_to_slack_within_3_seconds,
        lazy=[list_user_posted_review_action],
    )
