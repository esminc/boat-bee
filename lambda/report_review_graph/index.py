import json
import logging
import os

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
        df = load_items_from_dynamodb("review")

        file_path = "/tmp/review_graph.png"

        generate_review_graph(df, file_path)

        upload_file_to_slack(
            SLACK_BOT_TOKEN, SLACK_CHANNEL, file_path, "レビュー投稿数のグラフを更新しました"
        )
    except Exception as e:
        post_message_to_slack(SLACK_BOT_TOKEN, SLACK_CHANNEL, "レビュー投稿数のグラフの更新に失敗しました")

        logger.error("Error updating review graph: {}".format(e))


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


def generate_review_graph(df_review: pd.DataFrame, png_file_name: str):
    """
    reviewの時系列グラフを作成し、画像ファイルとして保存する
    """

    df_review["updated_at"] = df_review["updated_at"].map(lambda x: x[:10])

    df_review = (
        df_review["updated_at"].value_counts().sort_index().to_frame().reset_index()
    )

    df_review["type"] = "review_count"
    df_review = df_review.rename(columns={"updated_at": "count"})

    df_sum = df_review["count"].cumsum().to_frame()
    df_sum["index"] = df_review["index"]

    df_sum["type"] = "review_count_sum"

    df_review = pd.concat([df_review, df_sum]).reset_index()

    sns.set(rc={"figure.figsize": (30, 16)})

    plot = sns.lineplot(data=df_review, x="index", y="count", hue="type")
    plot.set_title("review count")
    plot.set_xlabel("date")

    plot.get_figure().savefig(png_file_name)
