import base64
import gzip
import json
import logging
import os

import boto3
from slack_sdk import WebhookClient

secretsmanager = boto3.client("secretsmanager")
secret_id = os.environ["SLACK_CREDENTIALS_SECRET_ID"]
secret_value = secretsmanager.get_secret_value(SecretId=secret_id)
secret = json.loads(secret_value["SecretString"])

SLACK_WEBHOOK_URL = secret["BEE_OPERATION_BOT_SLACK_WEBHOOK_URL"]


def lambda_handler(event, context):
    data = event["awslogs"]["data"]

    compressed_payload = base64.b64decode(data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)

    client = WebhookClient(SLACK_WEBHOOK_URL)

    text = "エラーを検出しました"
    text = text + "\n\n"
    text = text + "logStream: \n" + payload["logStream"]
    text = text + "\n\n"
    text = (
        text
        + "logEvents: \n"
        + "\n".join([str(log_event) for log_event in payload["logEvents"]])
    )

    response = client.send(text=text)

    logger = logging.getLogger()

    logger.info("Webhook Response: " + str(response))
