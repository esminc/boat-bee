import json


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
                    "action_id": "action_id_book_title",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "本のタイトルを入力してください",
                        "emoji": True,
                    },
                },
            },
            {
                "type": "image",
                "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
                "alt_text": "",
            },
        ],
    }


def post_review_modal(*, callback_id: str, book_section, url: str):
    """
    レビュー投稿モーダル

    Args:
        callback_id: モーダルのcallback_id
        book_section: レビューを投稿する本のsection block
        url: レビューを投稿する本のurl
    """

    private_metadata = json.dumps({"url": url})

    return {
        "type": "modal",
        "callback_id": callback_id,
        "private_metadata": private_metadata,
        "title": {"type": "plain_text", "text": "Bee"},
        "close": {"type": "plain_text", "text": "戻る", "emoji": True},
        "submit": {"type": "plain_text", "text": "送信"},
        "blocks": [
            {
                "type": "image",
                "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
                "alt_text": "",
            },
            book_section,
            {
                "type": "input",
                "block_id": "input_score_for_me",
                "label": {"type": "plain_text", "text": "自分にとっての評価"},
                "element": {
                    "type": "static_select",
                    "action_id": "action_id_score_for_me",
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
                    "action_id": "action_id_score_for_others",
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
                    "action_id": "action_id_comment",
                    "multiline": True,
                },
            },
        ],
    }
