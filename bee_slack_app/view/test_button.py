def generate_test_button_model_view(callback_id: str, interested: bool):
    """
    ボタンのテスト用モーダル

    Args:
        callback_id: モーダルのcallback_id
    """
    blocks = []
    button_name = "興味あり１" if interested else "興味なし１"
    blocks.append(
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": button_name,
                        "emoji": True,
                    },
                    "value": "dummy_value",
                    "action_id": "test_button_switch_action",
                },
            ],
        },
    )

    view = {
        "type": "modal",
        "callback_id": callback_id,
        "private_metadata": button_name,
        "title": {"type": "plain_text", "text": "ボタンの切り替えテスト"},
        "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
        "blocks": blocks,
    }
    return view
