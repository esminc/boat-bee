import gzip
import json
import logging
import os

import boto3
import pandas as pd
from boto3.dynamodb.types import TypeDeserializer

DYNAMODB_TABLE_JSON_GZ_FILE = "/tmp/dynamodb.json.gz"
JSON_FILE = "/tmp/dynamodb.json"


def lambda_handler(event, context):
    logger = logging.getLogger()

    dynamodb_export_id = event["DynamoDBExportId"]

    logger.info({"dynamodb_export_id": dynamodb_export_id})

    _download_dynamodb_json_from_s3(
        bucket=os.environ["DYNAMODB_EXPORT_BUCKET"],
        manifest_summary_key=f"AWSDynamoDB/{dynamodb_export_id}/manifest-files.json",
        file_to_download_to=DYNAMODB_TABLE_JSON_GZ_FILE,
    )

    _convert_dynamodb_json_to_json(
        input_json_gz=DYNAMODB_TABLE_JSON_GZ_FILE, output_json=JSON_FILE
    )

    _upload_json_to_s3(
        bucket=os.environ["CONVERTED_DYNAMODB_JSON_BUCKET"],
        item_key="dynamodb_table.json",
        json_file=JSON_FILE,
    )


def _download_dynamodb_json_from_s3(
    *, bucket: str, manifest_summary_key: str, file_to_download_to: str
) -> None:
    s3 = boto3.client("s3")

    manifest_summary_json_file = "/tmp/manifest_summary.json"

    s3.download_file(bucket, manifest_summary_key, manifest_summary_json_file)

    data_file_key = None

    with open(manifest_summary_json_file) as f:
        json_data = json.load(f)
        data_file_key = json_data["dataFileS3Key"]

    s3.download_file(bucket, data_file_key, file_to_download_to)


def _convert_dynamodb_json_to_json(*, input_json_gz: str, output_json: str) -> None:
    def _from_dynamodb_json_to_json(item):
        td = TypeDeserializer()
        return {k: td.deserialize(value=v) for k, v in item.items()}

    df = None

    with gzip.open(input_json_gz, "rt") as f:

        df = pd.read_json(f, orient="records", lines=True)

        json_data = df.applymap(lambda x: _from_dynamodb_json_to_json(x))[
            "Item"
        ].to_list()

        df = pd.DataFrame(json_data)

    df.to_json(output_json)


def _upload_json_to_s3(*, bucket: str, item_key: str, json_file: str) -> None:
    s3 = boto3.client("s3")

    s3.upload_file(json_file, bucket, item_key)
