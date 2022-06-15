import os

from bee_slack_app.service import review_service


def hello_controller(app):
    @app.message("hello")
    def message_hello(message, say):
        # say() sends a message to the channel where the event was triggered
        say(f"Hey there!! <@{message['user']}>!")

    @app.message("myreview")
    def show_my_review(ack, message, client):

        ack()

        user_id = message["user"]
        myreviews = [
            x["book_title"]
            for x in review_service.get_reviews_by_user_id(user_id=user_id)
        ]
        num_reviews = len(myreviews)
        myreviews = "\n・".join(myreviews)
        myreviews = f"・{myreviews}"

        client.chat_postEphemeral(
            channel=os.environ["NOTIFY_POST_REVIEW_CHANNEL"],
            user=user_id,
            text=f"<@{user_id}>さんが投稿したレビューはこれです（{num_reviews}冊）\n\n {myreviews}",
        )
