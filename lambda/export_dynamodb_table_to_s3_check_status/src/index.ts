import {
  DynamoDBClient,
  DescribeExportCommand,
} from "@aws-sdk/client-dynamodb";
import { Context } from "aws-lambda";

// rome-ignore lint:
export async function handler(event: any, context: Context) {
  const exportArn = event.Payload.DynamoDBExportArn;

  const client = new DynamoDBClient({});

  const command = new DescribeExportCommand({
    ExportArn: exportArn,
  });

  const { ExportDescription } = await client.send(command);

  const exportStatus = ExportDescription?.ExportStatus;

  console.log({ exportStatus });

  return { exportStatus, DynamoDBExportArn: exportArn };
}
