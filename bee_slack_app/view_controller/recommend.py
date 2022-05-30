from typing import Optional

from bee_slack_app.model.search import SearchedBook
from bee_slack_app.model.user import User
from bee_slack_app.service.recommend import recommend
from bee_slack_app.service.user import get_user
from bee_slack_app.service.user_action import record_user_action
from bee_slack_app.view.recommend import generate_book_recommend_model_view


def recommend_controller(app):  # pylint: disable=too-many-statements
    @app.action("book_recommend_action")
    def open_recommend_modal(ack, body, client, logger):
        ack()

        logger.info(body)

        user_id = body["user"]["id"]

        user: Optional[User] = get_user(logger, user_id)
        if not user:
            record_user_action(
                user_id=user_id,
                action_name="book_recommend_action",
                status="no_user_profile_error",
            )

            client.views_open(
                trigger_id=body["trigger_id"],
                view={
                    "type": "modal",
                    "title": {
                        "type": "plain_text",
                        "text": "プロフィールを入力してください",
                        "emoji": True,
                    },
                    "close": {"type": "plain_text", "text": "OK", "emoji": True},
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "おすすめ本を見るには、プロフィールの入力が必要です :bow:",
                            },
                        },
                    ],
                },
            )
            return

        book: Optional[SearchedBook] = recommend(logger, user)

        if book is None:
            record_user_action(
                user_id=user_id,
                action_name="book_recommend_action",
                status="no_recommended_book_error",
            )

            client.views_open(
                trigger_id=body["trigger_id"],
                view={
                    "type": "modal",
                    "title": {
                        "type": "plain_text",
                        "text": "おすすめの本は見つかりませんでした",
                        "emoji": True,
                    },
                    "close": {"type": "plain_text", "text": "OK", "emoji": True},
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "アプリ管理者にお問い合わせください :bow:",
                            },
                        },
                    ],
                },
            )
            return

        modal_view = generate_book_recommend_model_view(
            callback_id="book_recommend_modal", book=book
        )

        record_user_action(
            user_id=user_id,
            action_name="book_recommend_action",
            payload={"book": book},
        )

        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )
