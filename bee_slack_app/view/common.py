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
