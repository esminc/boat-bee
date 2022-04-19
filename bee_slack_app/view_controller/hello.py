from bee_slack_app import ml


def hello_controller(app):
    @app.message("hello")
    def message_hello(message, say):
        # say() sends a message to the channel where the event was triggered
        say(f"Hey there!! <@{message['user']}>!")

    @app.message("predict")
    def message_predict(_, say):

        predicted = ml.predict()

        say(f"predicted = {predicted}")
