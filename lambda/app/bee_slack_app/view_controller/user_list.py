from slack_bolt import App

from bee_slack_app.service.user import get_users_posted_review
from bee_slack_app.view import posted_review_user_list_modal


def user_list_controller(app: App) -> None:
    @app.action("list_user_posted_review_action")
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
