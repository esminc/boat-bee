import os
from typing import Any

import boto3  # type: ignore

PK = "PK"

GSI_0 = "GSI_0"
GSI_1 = "GSI_1"
GSI_2 = "GSI_2"
GSI_3 = "GSI_3"
GSI_PK = "GSI_PK"
GSI_0_SK = "GSI_0_SK"
GSI_1_SK = "GSI_1_SK"
GSI_2_SK = "GSI_2_SK"
GSI_3_SK = "GSI_3_SK"

DynamoDBResource = Any


def get_database_client() -> DynamoDBResource:
    """
    環境変数にDYNAMODB_ENDPOINTが設定されていればそこに接続する（ローカル環境）
    設定されていなければデフォルトのDynamoDBに接続する（AWSの環境）
    """
    endpoint_url = os.getenv("DYNAMODB_ENDPOINT", None)
    dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)

    return dynamodb


DynamoDBTable = Any


def get_table() -> DynamoDBTable:
    return get_database_client().Table(os.environ["DYNAMODB_TABLE"])


def create_table():
    """
    テスト用にテーブルを作成する
    """
    dynamodb = boto3.resource("dynamodb")

    return dynamodb.create_table(
        TableName=os.environ["DYNAMODB_TABLE"],
        AttributeDefinitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "GSI_PK", "AttributeType": "S"},
            {"AttributeName": "GSI_0_SK", "AttributeType": "S"},
            {"AttributeName": "GSI_1_SK", "AttributeType": "S"},
            {"AttributeName": "GSI_2_SK", "AttributeType": "S"},
            {"AttributeName": "GSI_3_SK", "AttributeType": "N"},
        ],
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        GlobalSecondaryIndexes=[
            {
                "IndexName": "GSI_0",
                "KeySchema": [
                    {"AttributeName": "GSI_PK", "KeyType": "HASH"},
                    {"AttributeName": "GSI_0_SK", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "GSI_1",
                "KeySchema": [
                    {"AttributeName": "GSI_PK", "KeyType": "HASH"},
                    {"AttributeName": "GSI_1_SK", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "GSI_2",
                "KeySchema": [
                    {"AttributeName": "GSI_PK", "KeyType": "HASH"},
                    {"AttributeName": "GSI_2_SK", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "GSI_3",
                "KeySchema": [
                    {"AttributeName": "GSI_PK", "KeyType": "HASH"},
                    {"AttributeName": "GSI_3_SK", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
    )
