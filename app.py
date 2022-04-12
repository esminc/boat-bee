import json
import os

import logging

import awsgi  # type: ignore
import app_local
import boto3  # type: ignore

logging.basicConfig(level=logging.DEBUG)

secretsmanager_client = boto3.client("secretsmanager", region_name="us-east-1")
secret_value = secretsmanager_client.get_secret_value(SecretId="slack_secret")
secret = json.loads(secret_value["SecretString"])

os.environ["SLACK_APP_TOKEN"] = secret["SLACK_APP_TOKEN"]
os.environ["SLACK_BOT_TOKEN"] = secret["SLACK_BOT_TOKEN"]
os.environ["SLACK_SIGNING_SECRET"] = secret["SLACK_SIGNING_SECRET"]

flask_app = app_local.flask_app

def lambda_handler(event, context):
    return awsgi.response(flask_app, event, context)
