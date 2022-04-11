import logging

import awsgi  # type: ignore

logging.basicConfig(level=logging.DEBUG)

from bee_slack_app.env import (  # pylint: disable=wrong-import-position
    configure_env_values,
)

configure_env_values()

from bee_slack_app.flask_app import flask_app  # pylint: disable=wrong-import-position


def lambda_handler(event, context):
    return awsgi.response(flask_app, event, context)
