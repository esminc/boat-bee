import json
import logging
import os

import boto3
import pandas as pd
from slack_sdk import WebhookClient

secretsmanager = boto3.client("secretsmanager")
secret_id = os.environ["SLACK_CREDENTIALS_SECRET_ID"]
secret_value = secretsmanager.get_secret_value(SecretId=secret_id)
secret = json.loads(secret_value["SecretString"])

SLACK_WEBHOOK_URL = secret["BEE_OPERATION_BOT_SLACK_WEBHOOK_URL"]


def lambda_handler(event, context):

    df = load_items_from_dynamodb("suggested_book")

    df_interested = df[df["interested"] == True]

    text = "レポート"
    text = text + "\n"
    text = text + "\n"
    text = text + "本がおすすめされた回数: " + str(len(df))
    text = text + "\n"
    text = text + "本が興味ありとされた回数: " + str(len(df_interested))
    text = text + "\n"
    text = text + "興味ありとされた本の数: " + str(len(pd.unique(df_interested["isbn"])))
    text = text + "\n"
    text = text + "本をおすすめされたことのあるユーザ数: " + str(len(pd.unique(df["user_id"])))
    text = text + "\n"
    text = text + "興味ありを一度でも押下したユーザ数: " + str(len(pd.unique(df_interested["user_id"])))
    text = text + "\n"

    client = WebhookClient(SLACK_WEBHOOK_URL)
    response = client.send(text=text)

    logger = logging.getLogger()

    logger.info("Webhook Response: " + str(response))


def load_items_from_dynamodb(item_id: str) -> pd.DataFrame:
    """
    DynamoDBからアイテムを取得する

    Args:
        item_id: アイテムの種別を表すキー。review、user、bookなど。
    """
    dynamodb_json_file = "/tmp/dynamodb_table.json"

    s3 = boto3.client("s3")

    s3.download_file(
        os.environ["CONVERTED_DYNAMODB_JSON_BUCKET"],
        "dynamodb_table.json",
        dynamodb_json_file,
    )

    df = None

    with open(dynamodb_json_file, "rt") as f:
        df = pd.read_json(f)

    return df[df["GSI_PK"] == item_id].reset_index()
