import json
import logging
import os
from typing import Any

import boto3
import pandas as pd
from slack_sdk import WebhookClient

secretsmanager = boto3.client("secretsmanager")
secret_id = os.environ["SLACK_CREDENTIALS_SECRET_ID"]
secret_value = secretsmanager.get_secret_value(SecretId=secret_id)
secret = json.loads(secret_value["SecretString"])

SLACK_WEBHOOK_URL = secret["BEE_OPERATION_BOT_SLACK_WEBHOOK_URL"]


def lambda_handler(event, context):
    suggested_books = load_items_from_dynamodb("suggested_book")

    df = pd.DataFrame(suggested_books)

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


def load_items_from_dynamodb(item_id: str) -> list[Any]:
    """
    DynamoDBからアイテムを取得する

    Args:
        item_id: アイテムの種別を表すキー。review、user、bookなど。
    """
    dynamodb = boto3.resource("dynamodb")

    def query(exclusive_start_key=None):
        option = {}
        if exclusive_start_key:
            option["ExclusiveStartKey"] = exclusive_start_key

        response = dynamodb.Table(os.environ["DYNAMODB_TABLE"]).query(
            IndexName="GSI_0",
            KeyConditionExpression=boto3.dynamodb.conditions.Key("GSI_PK").eq(item_id),
            **option,
        )

        return response["Items"], response.get("LastEvaluatedKey")

    items, last_key = query()

    # レスポンスに LastEvaluatedKey が含まれなくなるまでループ処理を実行する
    # see https://dev.classmethod.jp/articles/hot-to-get-more-than-1mb-of-data-from-dynamodb-when-using-scan/
    while last_key is not None:
        new_items, last_key = query(exclusive_start_key=last_key)
        items.extend(new_items)

    return items
