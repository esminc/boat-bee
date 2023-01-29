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
        df = load_items_from_dynamodb("user_action")

        file_path = "/tmp/user_action_graph.png"

        generate_user_action_graph(df, file_path)

        upload_file_to_slack(
            SLACK_BOT_TOKEN, SLACK_CHANNEL, file_path, "ユーザの行動履歴グラフを更新しました"
        )
    except Exception as e:
        post_message_to_slack(SLACK_BOT_TOKEN, SLACK_CHANNEL, "ユーザの行動履歴グラフの更新に失敗しました")

        logger.error("Error updating user action graph: {}".format(e))


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


def generate_user_action_graph(
    df_user_action: pd.DataFrame, png_file_name: str
) -> None:
    """
    user_actionの時系列グラフを作成し、画像ファイルとして保存する
    """
    df = _make_user_action_count_frame(df_user_action)

    sns.set(rc={"figure.figsize": (30, 16)})

    plot = sns.lineplot(data=df, x="index", y="created_at_date", hue="action")

    plot.set_title("user action")
    plot.set_xlabel("date")
    plot.set_ylabel("action count")

    plot.get_figure().savefig(png_file_name)


def _make_user_action_count_frame(df_user_action: pd.DataFrame):
    """
    user_actionを日時ごとにカウントしたデータフレームを、user_action別で作成する
    """

    # 全てのuser_actionを集計する
    df = _make_user_action_count_frame_one(df_user_action, "all")

    action_name_list = [
        "post_review_action",
        "post_review_modal",
        "app_home_opened",
        "book_search_modal",
        "book_search_result_modal",
        "read_review_of_book_action",
        "read_review_of_user_action",
        "open_review_detail_modal_action",
        "user_info_action",
        "user_profile_modal",
    ]

    # 個別のuser_actionを集計する
    for action_name in action_name_list:

        df_specific_user_action = df_user_action[
            df_user_action["action_name"] == action_name
        ]

        if df_specific_user_action.empty:
            continue

        df_tmp = _make_user_action_count_frame_one(df_specific_user_action, action_name)

        df = pd.concat([df, df_tmp])

    return df.reset_index()


def _make_user_action_count_frame_one(df_user_action: pd.DataFrame, action):
    """
    user_actionを日時ごとにカウントしたデータフレームを作成する
    """

    df_user_action["created_at_date"] = df_user_action["created_at"].map(
        lambda x: x[:10]
    )

    df = (
        df_user_action["created_at_date"]
        .value_counts()
        .sort_index()
        .to_frame()
        .reset_index()
    )
    df["action"] = action

    return df
