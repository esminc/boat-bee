import json
import os

import boto3  # type: ignore
from slack_bolt import App

secretsmanager_client = boto3.client("secretsmanager", region_name="us-east-1")
secret_value = secretsmanager_client.get_secret_value(SecretId="slack_secret")
secret = json.loads(secret_value["SecretString"])

os.environ["SLACK_APP_TOKEN"] = secret["SLACK_APP_TOKEN"]
os.environ["SLACK_BOT_TOKEN"] = secret["SLACK_BOT_TOKEN"]
os.environ["SLACK_SIGNING_SECRET"] = secret["SLACK_SIGNING_SECRET"]


app = App(process_before_response=True)


@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")
