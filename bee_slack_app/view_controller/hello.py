def hello_controller(app):
    @app.message("hello")
    def message_hello(message, say):
        # say() sends a message to the channel where the event was triggered
        say(f"Hey there!! <@{message['user']}>!")
