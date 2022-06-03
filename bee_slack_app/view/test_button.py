import json


def generate_test_button_model_view(
    callback_id: str,
    interested: list[bool],
):
    """
    ボタンのテスト用モーダル

    Args:
        callback_id: モーダルのcallback_id
    """
    blocks = []

    for i, button_status in enumerate(interested):
        create_button(button_status, blocks, i)

    interested_dict = {"interested": interested}

    # private_metadataに格納するために文字列に変換する
    private_metadata = json.dumps(interested_dict)

    view = {
        "type": "modal",
        "callback_id": callback_id,
        "private_metadata": private_metadata,
        "title": {"type": "plain_text", "text": "ボタンの切り替えテスト"},
        "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
        "blocks": blocks,
    }
    return view


def create_button(interested: bool, blocks: list, button_value: int):
    button_name = "興味あり" if interested else "興味なし"
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
                    "value": str(button_value),
                    "action_id": "test_button_switch_action",
                },
            ],
        },
    )
