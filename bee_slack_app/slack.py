from slack_bolt import App

from bee_slack_app import ml

app = App(process_before_response=True)


@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

@app.message("レビュー")
def message_review(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"レビューします <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.action("button_click")
def open_modal(ack, body, client):
    # コマンドのリクエストを確認
    ack()
    # 組み込みのクライアントで views_open を呼び出し
    client.views_open(
        # 受け取りから 3 秒以内に有効な trigger_id を渡す
        trigger_id=body["trigger_id"],
        # ビューのペイロード
        view={
            "type": "modal",
            # ビューの識別子
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text":"My App"},
            "submit": {"type": "plain_text", "text":"送信"},
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text":"Welcome to a modal with _blocks_"},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text":"Click me!"},
                        "action_id": "button_abc"
                    }
                },
                {
                    "type": "input",
                    "block_id": "input_c",
                    "label": {"type": "plain_text", "text":"What are your hopes and dreams?"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "dreamy_input",
                        "multiline":True
                    }
                }
            ]
        }
    )

@app.message("predict")
def message_predict(_, say):

    predicted = ml.predict()

    say(f"predicted = {predicted}")
