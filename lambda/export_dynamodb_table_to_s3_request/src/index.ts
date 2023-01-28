import {
  DynamoDBClient,
  ExportTableToPointInTimeCommand,
} from "@aws-sdk/client-dynamodb";
import { Context } from "aws-lambda";

// rome-ignore lint:
export async function handler(event: any, context: Context) {
  const client = new DynamoDBClient({});

  const command = new ExportTableToPointInTimeCommand({
    TableArn: process.env.DYNAMODB_TABLE_ARN,
    S3Bucket: process.env.S3_BUCKET_NAME,
  });

  const { ExportDescription } = await client.send(command);

  return { DynamoDBExportArn: ExportDescription?.ExportArn };
}
