import json
import os

import boto3  # type: ignore


def configure_env_values():

    secretsmanager_client = boto3.client("secretsmanager", region_name="us-east-1")

    stage = os.environ["SERVERLESS_STAGE"]

    secret_id = None
    if stage == "dev":
        secret_id = "slack_secret"
    elif stage in ["stage-a", "stage-b", "stage-c", "stage-d"]:
        secret_id = f"slack_secret_{stage}"
    else:
        secret_id = "slack_secret"

    secret_value = secretsmanager_client.get_secret_value(SecretId=secret_id)
    secret = json.loads(secret_value["SecretString"])

    os.environ["SLACK_APP_TOKEN"] = secret["SLACK_APP_TOKEN"]
    os.environ["SLACK_BOT_TOKEN"] = secret["SLACK_BOT_TOKEN"]
    os.environ["SLACK_SIGNING_SECRET"] = secret["SLACK_SIGNING_SECRET"]
