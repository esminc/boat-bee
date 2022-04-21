import os

import boto3  # type: ignore


def get_database_client():
    """
    環境変数にDYNAMODB_ENDPOINTが設定されていればそこに接続する（ローカル環境）
    設定されていなければデフォルトのDynamoDBに接続する（AWSの環境）
    """
    endpoint_url = os.getenv("DYNAMODB_ENDPOINT", None)
    dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)

    return dynamodb
