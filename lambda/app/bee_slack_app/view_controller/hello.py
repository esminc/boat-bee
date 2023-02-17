import os

from slack_bolt import App

from bee_slack_app.service import review_service
from bee_slack_app.utils.timer import StopWatch, location  # type: ignore


def hello_controller(app: App) -> None:
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

        myreviews_str = "\n・".join(myreviews)
        myreviews_str = f"・{myreviews_str}"

        client.chat_postEphemeral(
            channel=os.environ["NOTIFY_POST_REVIEW_CHANNEL"],
            user=user_id,
            text=f"<@{user_id}>さんがレビューを投稿した本の一覧です（{num_reviews}冊）\n\n {myreviews_str}",
        )

    @app.command("/bee")
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

            myreviews_str = "\n・".join(myreviews)
            myreviews_str = f"・{myreviews_str}"

            respond(
                f"<@{user_id}>さんがレビューを投稿した本の一覧です（{num_reviews}冊）\n\n {myreviews_str}"
            )
            return

        respond(
            f"{command_text} は、利用可能なサブコマンドではありません。\n\n利用可能なサブコマンドは下記の通りです。\n- myreview : 自分の投稿したレビューを確認する"
        )
