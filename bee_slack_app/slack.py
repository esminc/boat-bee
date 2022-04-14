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
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Check out these rad radio buttons"
                    },
                    "accessory": {
                        "type": "radio_buttons",
                        "action_id": "this_is_an_action_id",
                        "initial_option": {
                            "value": "A1",
                            "text": {
                                "type": "plain_text",
                                "text": "評価1"
                            }
                        },
                        "options": [
                            {
                                "value": "A1",
                                "text": {
                                "type": "plain_text",
                                "text": "評価1"
                                }
                            },
                            {
                                "value": "A2",
                                "text": {
                                "type": "plain_text",
                                "text": "評価2"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    )

# view_submission リクエストを処理
@app.view("view_1")
def handle_submission(ack, body, client, view, logger):
    print("ビューからのイベント")
    # `input_c`という block_id に `dreamy_input` を持つ input ブロックがある場合
    hopes_and_dreams = view["state"]["values"]["input_c"]["dreamy_input"]
    print(hopes_and_dreams)
    user = body["user"]["id"]
    # 入力値を検証
    errors = {}
    if hopes_and_dreams is not None and len(hopes_and_dreams) <= 1:
        errors["input_c"] = "The value must be longer than 5 characters"
    if len(errors) > 0:
        ack(response_action="errors", errors=errors)
        return
    # view_submission リクエストの確認を行い、モーダルを閉じる
    ack()
    # 入力されたデータを使った処理を実行。このサンプルでは DB に保存する処理を行う
    # そして入力値の検証結果をユーザーに送信

    # ユーザーに送信するメッセージ
    msg = ""
    try:
        # DB に保存
        msg = f"Your submission of {hopes_and_dreams} was successful"
    except Exception as e:
        # エラーをハンドリング
        msg = "There was an error with your submission"

    # ユーザーにメッセージを送信
    try:
        client.chat_postMessage(channel=user, text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")



@app.message("predict")
def message_predict(_, say):

    predicted = ml.predict()

    say(f"predicted = {predicted}")
