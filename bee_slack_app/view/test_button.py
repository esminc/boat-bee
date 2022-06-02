def generate_test_button_model_view(callback_id: str):
    """
    おすすめ本モーダル

    Args:
        callback_id: モーダルのcallback_id
    """
    blocks = []
    blocks.append(
        {
            "type": "image",
            "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
            "alt_text": "",
        },
    )

    view = {
        "type": "modal",
        "callback_id": callback_id,
        "title": {"type": "plain_text", "text": "あなたへのおすすめ本"},
        "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
        "blocks": blocks,
    }
    return view
