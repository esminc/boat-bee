import logging

import awsgi  # type: ignore

# TODO: slack.pyの型情報をmypyで参照できるようにする
from bee_slack_app import slack  # type: ignore
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

logging.basicConfig(level=logging.DEBUG)


flask_app = Flask(__name__)


handler = SlackRequestHandler(slack.app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


def lambda_handler(event, context):
    return awsgi.response(flask_app, event, context)
