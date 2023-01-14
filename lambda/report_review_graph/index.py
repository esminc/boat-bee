import json
import logging
import os
from typing import Any

import boto3
import pandas as pd
import seaborn as sns
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

secretsmanager = boto3.client("secretsmanager")
secret_id = os.environ["SLACK_CREDENTIALS_SECRET_ID"]
secret_value = secretsmanager.get_secret_value(SecretId=secret_id)
secret = json.loads(secret_value["SecretString"])

SLACK_BOT_TOKEN = secret["BEE_OPERATION_BOT_SLACK_BOT_TOKEN"]
SLACK_CHANNEL = secret["BEE_OPERATION_BOT_SLACK_CHANNEL"]


def lambda_handler(event, context):
    logger = logging.getLogger()

    try:
        items = load_items_from_dynamodb("review")

        file_path = "/tmp/review_graph.png"

        generate_review_graph(items, file_path)

        upload_file_to_slack(
            SLACK_BOT_TOKEN, SLACK_CHANNEL, file_path, "レビュー投稿数のグラフを更新しました"
        )
    except Exception as e:
        post_message_to_slack(SLACK_BOT_TOKEN, SLACK_CHANNEL, "レビュー投稿数のグラフの更新に失敗しました")

        logger.error("Error updating review graph: {}".format(e))


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


def upload_file_to_slack(
    slack_token: str, channel: str, file_name: str, message: str
) -> None:
    """
    Slackのチャンネルにファイルをアップロードする
    """
    logger = logging.getLogger()

    try:
        client = WebClient(token=slack_token)

        client.files_upload(
            channels=channel,
            initial_comment=message,
            file=file_name,
        )

    except SlackApiError as e:
        logger.error("Error uploading file: {}".format(e))


def post_message_to_slack(slack_token: str, channel: str, message: str) -> None:
    """
    Slackのチャンネルにメッセージを送信する
    """
    logger = logging.getLogger()

    try:
        client = WebClient(token=slack_token)

        client.chat_postMessage(
            channel=channel,
            text=message,
        )

    except SlackApiError as e:
        logger.error("Error post message: {}".format(e))


def generate_review_graph(review_items: Any, png_file_name: str):
    """
    reviewの時系列グラフを作成し、画像ファイルとして保存する
    """

    df = pd.DataFrame(review_items)

    df["updated_at"] = df["updated_at"].map(lambda x: x[:10])

    df = df["updated_at"].value_counts().sort_index().to_frame().reset_index()

    df["type"] = "review_count"
    df = df.rename(columns={"updated_at": "count"})

    df_sum = df["count"].cumsum().to_frame()
    df_sum["index"] = df["index"]

    df_sum["type"] = "review_count_sum"

    df = pd.concat([df, df_sum]).reset_index()

    sns.set(rc={"figure.figsize": (30, 16)})

    plot = sns.lineplot(data=df, x="index", y="count", hue="type")
    plot.set_title("review count")
    plot.set_xlabel("date")

    plot.get_figure().savefig(png_file_name)
