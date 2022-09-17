import { App, AwsLambdaReceiver } from "@slack/bolt";
import {
  SecretsManagerClient,
  GetSecretValueCommand,
} from "@aws-sdk/client-secrets-manager";
import { HelloController } from "./src/view_controller";

type AwsHandler = Awaited<ReturnType<AwsLambdaReceiver["start"]>>;

export const handler: AwsHandler = async (event, context, callback) => {
  const client = new SecretsManagerClient({ region: "us-east-1" });

  const SecretId = process.env["SLACK_CREDENTIALS_SECRET_ID"];

  const command = new GetSecretValueCommand({ SecretId });

  const { SecretString } = await client.send(command);

  if (!SecretString) {
    throw new Error(
      "Failed to retrieve Slack Credentials from Secret Manager."
    );
  }

  const { SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET } = JSON.parse(SecretString);

  if (!SLACK_SIGNING_SECRET) {
    throw new Error("SLACK_SIGNING_SECRET is required.");
  }

  if (!SLACK_BOT_TOKEN) {
    throw new Error("SLACK_BOT_TOKEN is required.");
  }

  const awsLambdaReceiver = new AwsLambdaReceiver({
    signingSecret: SLACK_SIGNING_SECRET,
  });

  const app = new App({
    token: SLACK_BOT_TOKEN,
    receiver: awsLambdaReceiver,
  });

  HelloController(app);

  const handler = await awsLambdaReceiver.start();
  return handler(event, context, callback);
};
