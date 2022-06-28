import os

from bee_slack_app.service import review_service
from bee_slack_app.utils.timer import StopWatch, location


def hello_controller(app):
    @app.message("hello")
    def message_hello(message, say):
        # say() sends a message to the channel where the event was triggered
        with StopWatch(location()):
            say(f"Hey there!! <@{message['user']}>!")

    @app.message("myreview")
    def show_my_review(ack, message, client):

        ack()

        user_id = message["user"]
        myreviews = [
            x["book_title"]
            for x in sorted(
                review_service.get_reviews_by_user_id(user_id=user_id),
                key=lambda x: x["updated_at"],
                reverse=True,
            )
        ]
        num_reviews = len(myreviews)

        if num_reviews == 0:
            client.chat_postEphemeral(
                channel=os.environ["NOTIFY_POST_REVIEW_CHANNEL"],
                user=user_id,
                text=f"<@{user_id}>さんはまだレビューを投稿していませんね",
            )
            return

        myreviews = "\n・".join(myreviews)
        myreviews = f"・{myreviews}"

        client.chat_postEphemeral(
            channel=os.environ["NOTIFY_POST_REVIEW_CHANNEL"],
            user=user_id,
            text=f"<@{user_id}>さんがレビューを投稿した本の一覧です（{num_reviews}冊）\n\n {myreviews}",
        )
