from bee_slack_app.model import ReviewContents
from bee_slack_app.utils import datetime
from bee_slack_app.view.common import book_section, google_logo_image


def search_book_to_review_modal(*, callback_id: str):
    """
    レビューする本を検索するモーダル

    Args:
        callback_id: モーダルのcallback_id
    """
    return {
        "type": "modal",
        "callback_id": callback_id,
        "title": {"type": "plain_text", "text": "レビューする本を検索する"},
        "submit": {"type": "plain_text", "text": "書籍の検索"},
        "blocks": [
            {
                "type": "input",
                "block_id": "input_book_title",
                "label": {"type": "plain_text", "text": "タイトル"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "book_title_action",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "本のタイトルを入力してください",
                        "emoji": True,
                    },
                },
            },
            google_logo_image(),
        ],
    }


def post_review_modal(*, callback_id: str, book_section_to_review):
    """
    レビュー投稿モーダル

    Args:
        callback_id: モーダルのcallback_id
        book_section_to_review: レビューを投稿する本のsection block
    """

    return {
        "type": "modal",
        "callback_id": callback_id,
        "title": {"type": "plain_text", "text": "Bee"},
        "close": {"type": "plain_text", "text": "戻る", "emoji": True},
        "submit": {"type": "plain_text", "text": "送信"},
        "blocks": [
            google_logo_image(),
            book_section_to_review,
            {
                "type": "input",
                "block_id": "input_score_for_me",
                "label": {"type": "plain_text", "text": "自分にとっての評価"},
                "element": {
                    "type": "static_select",
                    "action_id": "score_for_me_action",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "選択してください",
                        "emoji": True,
                    },
                    "options": [
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
                },
            },
            {
                "type": "input",
                "block_id": "input_score_for_others",
                "label": {"type": "plain_text", "text": "永和社員へのおすすめ度"},
                "element": {
                    "type": "static_select",
                    "action_id": "score_for_others_action",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "選択してください",
                        "emoji": True,
                    },
                    "options": [
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
                },
            },
            {
                "type": "input",
                "block_id": "input_comment",
                "label": {"type": "plain_text", "text": "レビューコメント"},
                "optional": True,
                "element": {
                    "type": "plain_text_input",
                    "action_id": "comment_action",
                    "multiline": True,
                },
            },
            {
                "type": "input",
                "block_id": "disable_notify_review_post_block",
                "optional": True,
                "label": {
                    "type": "plain_text",
                    "text": "チャンネル #bee へのレビュー投稿通知",
                    "emoji": True,
                },
                "element": {
                    "type": "checkboxes",
                    "action_id": "disable_notify_review_post_action",
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "レビュー投稿を通知しない",
                                "emoji": True,
                            },
                            "value": "disable_notify_review_post",
                        },
                    ],
                },
            },
        ],
    }


def notify_review_post_message_blocks(review_contents: ReviewContents):
    """
    レビュー投稿メッセージブロック

    Args:
        review_contents: 投稿したレビュー
    """

    update_datetime = (
        datetime.parse(review_contents["updated_at"])
        if review_contents["updated_at"]
        else "-"
    )

    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{review_contents['user_name']}さんがレビューを投稿しました :tada:",
                "emoji": True,
            },
        },
        book_section(
            title=review_contents["book_title"],
            author=review_contents["book_author"],
            isbn=review_contents["isbn"],
            url=review_contents["book_url"],
            image_url=review_contents["book_image_url"],
        ),
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*投稿者*\n{review_contents['user_name']}",
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
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*レビューコメント*\n\n{review_contents['review_comment'] or '-'}",
            },
        },
    ]
