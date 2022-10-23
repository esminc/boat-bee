import os

from bee_slack_app.service import review_service
from bee_slack_app.utils.timer import StopWatch, location
from bee_slack_app.view_controller.utils import respond_to_slack_within_3_seconds

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

    def repeat_text(ack, respond, command):
        ack()

        command_text = command.get("text")

        if not command_text:
            respond(
                "/bee <subcommand>の形式で実行してください。\n\n利用可能なサブコマンドは下記の通りです。\n- myreview : 自分の投稿したレビューを確認する"
            )
            return

        if command_text == "myreview":

            user_id = command["user_id"]
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
                respond(f"<@{user_id}>さんはまだレビューを投稿していませんね")
                return

            myreviews = "\n・".join(myreviews)
            myreviews = f"・{myreviews}"

            respond(f"<@{user_id}>さんがレビューを投稿した本の一覧です（{num_reviews}冊）\n\n {myreviews}")
            return

        respond(
            f"{command_text} は、利用可能なサブコマンドではありません。\n\n利用可能なサブコマンドは下記の通りです。\n- myreview : 自分の投稿したレビューを確認する"
        )

    app.command("/bee")(
        ack=respond_to_slack_within_3_seconds,
        lazy=[repeat_text],
    )
