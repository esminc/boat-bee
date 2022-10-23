import json
import os

import boto3  # type: ignore
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

SlackRequestHandler.clear_all_log_handlers()


secretsmanager_client = boto3.client("secretsmanager")

secret_id = os.environ["SLACK_CREDENTIALS_SECRET_ID"]

secret_value = secretsmanager_client.get_secret_value(SecretId=secret_id)
secret = json.loads(secret_value["SecretString"])

os.environ["SLACK_APP_TOKEN"] = secret["SLACK_APP_TOKEN"]
os.environ["SLACK_BOT_TOKEN"] = secret["SLACK_BOT_TOKEN"]
os.environ["SLACK_SIGNING_SECRET"] = secret["SLACK_SIGNING_SECRET"]
os.environ["NOTIFY_POST_REVIEW_CHANNEL"] = secret["NOTIFY_POST_REVIEW_CHANNEL"]


from bee_slack_app.slack import app  # pylint: disable=wrong-import-position


def lambda_handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
