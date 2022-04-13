import json
import logging
import os

import awsgi  # type: ignore
import boto3  # type: ignore

from bee_slack_app.flask_app import flask_app

logging.basicConfig(level=logging.DEBUG)

secretsmanager_client = boto3.client("secretsmanager", region_name="us-east-1")
secret_value = secretsmanager_client.get_secret_value(SecretId="slack_secret")
secret = json.loads(secret_value["SecretString"])

os.environ["SLACK_APP_TOKEN"] = secret["SLACK_APP_TOKEN"]
os.environ["SLACK_BOT_TOKEN"] = secret["SLACK_BOT_TOKEN"]
os.environ["SLACK_SIGNING_SECRET"] = secret["SLACK_SIGNING_SECRET"]


def lambda_handler(event, context):
    return awsgi.response(flask_app, event, context)
