from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

# TODO: slack.pyの型情報をmypyで参照できるようにする
from bee_slack_app.slack import app  # type: ignore

flask_app = Flask(__name__)


handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
