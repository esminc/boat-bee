import logging

from slack_bolt.adapter.aws_lambda import SlackRequestHandler

logging.basicConfig(level=logging.DEBUG)

from bee_slack_app.env import (  # pylint: disable=wrong-import-position
    configure_env_values,
)

configure_env_values()

from bee_slack_app.slack import app  # pylint: disable=wrong-import-position


def lambda_handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
