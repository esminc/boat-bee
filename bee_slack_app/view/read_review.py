from bee_slack_app.model.review import ReviewContents
from bee_slack_app.utils import datetime


def review_list_modal(
    *,
    callback_id: str,
    search_button_action_id: str,
    review_contents_list: list[ReviewContents],
    private_metadata=None,
    show_move_to_back=False,
    show_move_to_next=True,
):
    """
    レビューリストモーダル

    Args:
        callback_id: モーダルのcallback_id
        search_button_action_id: 「検索」ボタンのaction_id
        review_contents_list: 表示するレビューのリスト
        private_metadata: モーダルのprivate_metadata
        show_move_to_back: 「前へ」ボタンを表示するか
        show_move_to_next: 「次へ」ボタンを表示するか
    """
    review_list = []

    for review_contents in review_contents_list:

        # 空はエラーになるため、ハイフンを設定
        # TODO: 本来 review_comment が None になることは想定されていない（get_reviewsが返す型と不一致）なので、service側での修正が必要
        review_comment = review_contents["review_comment"]
        review_comment = (
            review_comment
            if review_comment is not None and len(review_comment) > 0
            else "-"
        )

        review_list.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{review_contents['book_title']}*\n{review_contents['book_author']}\nISBN-{review_contents['isbn']}\n<{review_contents['book_url']}|Google Booksで見る>",
                },
                "accessory": {
                    "type": "image",
                    "image_url": review_contents["book_image_url"],
                    "alt_text": review_contents["book_title"],
                },
            },
        )

        update_datetime = (
            datetime.parse(review_contents["updated_at"])
            if review_contents["updated_at"]
            else "-"
        )

        review_list.append(
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*投稿者*\n{review_contents['user_id']}",
                    },  # type:ignore
                    {
                        "type": "mrkdwn",
                        "text": f"*投稿日時*\n{update_datetime}",
                    },  # type:ignore
                    {  # type:ignore
                        "type": "mrkdwn",
                        "text": f"*自分にとっての評価*\n{review_contents['score_for_me']}",
                    },
                    {  # type:ignore
                        "type": "mrkdwn",
                        "text": f"*永和社員へのおすすめ度*\n{review_contents['score_for_others']}",
                    },
                ],
            }
        )

        review_list.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*レビューコメント*\n\n{review_comment}"},
            }
        )

        review_list.append({"type": "divider"})

    move_buttons = {
        "type": "actions",
        "elements": [],
    }

    if show_move_to_back:
        move_buttons["elements"] = [
            {  # type: ignore
                "type": "button",
                "text": {"type": "plain_text", "text": "前へ"},
                "action_id": "move_to_back",
            }
        ]

    if show_move_to_next:
        move_buttons["elements"] = move_buttons["elements"] + [  # type: ignore
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "次へ"},
                "action_id": "move_to_next",
            }
        ]

    return {
        "private_metadata": private_metadata or "[]",
        "type": "modal",
        "callback_id": callback_id,
        "title": {"type": "plain_text", "text": "Bee"},
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": "*検索条件*"}},
            {
                "block_id": "score_for_me_select_block",
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "自分にとっての評価",
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "未指定",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "value": "0",
                            "text": {"type": "plain_text", "text": "未指定"},
                        },
                        {
                            "value": "5",
                            "text": {"type": "plain_text", "text": "とても良い"},
                        },
                        {
                            "value": "4",
                            "text": {"type": "plain_text", "text": "良い"},
                        },
                        {
                            "value": "3",
                            "text": {"type": "plain_text", "text": "普通"},
                        },
                        {
                            "value": "2",
                            "text": {"type": "plain_text", "text": "悪い"},
                        },
                        {
                            "value": "1",
                            "text": {"type": "plain_text", "text": "とても悪い"},
                        },
                    ],
                    "action_id": "score_for_me_select_action",
                },
            },
            {
                "block_id": "score_for_others_select_block",
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "永和社員へのおすすめ度",
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "未指定",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "value": "0",
                            "text": {"type": "plain_text", "text": "未指定"},
                        },
                        {
                            "value": "5",
                            "text": {"type": "plain_text", "text": "とてもおすすめ"},
                        },
                        {
                            "value": "4",
                            "text": {"type": "plain_text", "text": "おすすめ"},
                        },
                        {
                            "value": "3",
                            "text": {"type": "plain_text", "text": "普通"},
                        },
                        {
                            "value": "2",
                            "text": {"type": "plain_text", "text": "おすすめしない"},
                        },
                        {
                            "value": "1",
                            "text": {"type": "plain_text", "text": "絶対におすすめしない"},
                        },
                    ],
                    "action_id": "score_for_others_select_action",
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "検索"},
                        "action_id": search_button_action_id,
                    },
                ],
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": "*検索結果*"}},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"{len(review_contents_list)}件"},
            },
            {"type": "divider"},
        ]
        + review_list  # type: ignore
        + [move_buttons],  # type: ignore
    }
