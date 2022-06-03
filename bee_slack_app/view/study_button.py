import json


def generate_test_button_model_view(
    callback_id: str,
    button_status_list: list[bool],
) -> dict:
    """
    ボタンのテスト用モーダル

    Args:
        callback_id: モーダルのcallback_id
    """
    blocks = []

    for i, button_status in enumerate(button_status_list):
        blocks.append(create_button(button_status, i))

    button_info = {"interested": button_status_list}

    # private_metadataに格納するために文字列に変換する
    private_metadata = json.dumps(button_info)

    view = {
        "type": "modal",
        "callback_id": callback_id,
        "private_metadata": private_metadata,
        "title": {"type": "plain_text", "text": "ボタンの切り替えテスト"},
        "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
        "blocks": blocks,
    }
    return view


def create_button(interested: bool, button_value: int) -> dict:
    button_name = "❤️興味あり" if interested else "🤍興味なし"
    return {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": button_name,
                    "emoji": True,
                },
                # valueにはstrしか格納できないため変換する
                # 取り出した側でintに戻して利用する
                "value": str(button_value),
                "action_id": "test_button_switch_action",
            },
        ],
    }
