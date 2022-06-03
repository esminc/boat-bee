def generate_test_button_model_view(callback_id: str, interested: bool):
    """
    ボタンのテスト用モーダル

    Args:
        callback_id: モーダルのcallback_id
    """
    blocks = []

    blocks.append(
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "興味あり１" if interested else "興味なし１",
                        "emoji": True,
                    },
                    "value": "dummy_value",
                    "action_id": "test_button_non_1_action",
                },
            ],
        },
    )

    view = {
        "type": "modal",
        "callback_id": callback_id,
        "title": {"type": "plain_text", "text": "ボタンの切り替えテスト"},
        "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
        "blocks": blocks,
    }
    return view
