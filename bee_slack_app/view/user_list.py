from bee_slack_app.model.user import User


def posted_review_user_list_modal(callback_id: str, users: list[User]):
    """
    レビューを投稿したユーザモーダル
    Args:
        callback_id: モーダルのcallback_id
        users: レビューを投稿したユーザ
    """
    view = {
        "type": "modal",
        "callback_id": callback_id,
        "title": {"type": "plain_text", "text": "レビューを投稿したユーザ"},
        "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
        "blocks": [],
    }

    if not users:
        view["blocks"] = [
            {  # type: ignore
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "ユーザの取得に失敗しました :expressionless:",
                    "emoji": True,
                },
            }
        ]
        return view

    users_blocks = []

    for user in users:
        users_blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{user['user_name']}* ({user['review_count']})",
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "このユーザのレビューを見る",
                        "emoji": True,
                    },
                    "value": user["user_id"],
                    "action_id": "read_review_of_user_action",
                },
            }
        )

    view["blocks"] = users_blocks  # type: ignore

    return view
