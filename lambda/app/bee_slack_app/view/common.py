import os
from typing import Optional


def simple_modal(
    *,
    title: str,
    text: str,
):
    """
    テキストだけの簡易モーダル

    Args:
        title: モーダルのタイトル
        text: モーダルの本文
    """
    return {
        "type": "modal",
        "title": {"type": "plain_text", "text": title, "emoji": True},
        "close": {"type": "plain_text", "text": "OK", "emoji": True},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": text,
                    "emoji": True,
                },
            },
        ],
    }


DUMMY_IMAGE_URL = os.environ["ASSET_URL"] + "/no_image.png"


def book_section(
    *, title: str, author: str, isbn: str, url: str, image_url: Optional[str] = None
):
    """
    本のセクション
    """
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*{title}*\n{author}\nISBN-{isbn}\n<{url}|Google Booksで見る>",
        },
        "accessory": {
            "type": "image",
            "image_url": image_url or DUMMY_IMAGE_URL,
            "alt_text": title,
        },
    }


def google_graphic():
    """
    「Powered by Google」
    """
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Powered by Google",
        },
    }
