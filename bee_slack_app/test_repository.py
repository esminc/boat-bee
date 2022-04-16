
from moto import mock_dynamodb
import boto3  # type: ignore
from bee_slack_app.repository import _BookReview, update
import pytest
import os
from boto3.dynamodb.conditions import Attr, Key


@mock_dynamodb
def test_レビューを作成できること():
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.create_table(
        TableName='dee-dev',
        KeySchema=[
            {
                'AttributeName': 'userId',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'userId',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    #table = dynamodb.Table('bee-dev')

    update()
    #bookReview = _BookReview()
    #bookReview.create()


    response = table.query(
        KeyConditionExpression=Key("userId").eq("test-id"),
    )

    assert len(response["Items"]) == 1, "レコード取得件数"

    actual_data = response["Items"][0]

    assert actual_data["userId"] == "test-id"
    assert actual_data["review_text"] == "This is a sample text."
