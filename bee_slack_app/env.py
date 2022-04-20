import json
import os

import boto3  # type: ignore


def configure_env_values():

    secretsmanager_client = boto3.client("secretsmanager", region_name="us-east-1")

    secret_id = os.environ["SLACK_CREDENTIALS_SECRET_ID"]

    secret_value = secretsmanager_client.get_secret_value(SecretId=secret_id)
    secret = json.loads(secret_value["SecretString"])

    os.environ["SLACK_APP_TOKEN"] = secret["SLACK_APP_TOKEN"]
    os.environ["SLACK_BOT_TOKEN"] = secret["SLACK_BOT_TOKEN"]
    os.environ["SLACK_SIGNING_SECRET"] = secret["SLACK_SIGNING_SECRET"]
