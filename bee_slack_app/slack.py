from slack_bolt import App

from bee_slack_app import ml
from bee_slack_app.repository import bookReview

app = App(process_before_response=True)


@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")


@app.message("predict")
def message_predict(_, say):

    predicted = ml.predict()

    say(f"predicted = {predicted}")


@app.message("database-test")
def db_create(_, say):
    item = bookReview.create()

    say(f"アイテムの作成が成功しました: {item}")
