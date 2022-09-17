import { App, AwsLambdaReceiver } from "@slack/bolt";
import {
  SecretsManagerClient,
  GetSecretValueCommand,
} from "@aws-sdk/client-secrets-manager";
import { HelloController } from "./src/view_controller";

const client = new SecretsManagerClient({ region: "us-east-1" });

const SecretId = process.env["SLACK_CREDENTIALS_SECRET_ID"];

const command = new GetSecretValueCommand({ SecretId });

//const data = await client.send(command);

const { SLACK_SIGNING_SECRET } = process.env;

if (!SLACK_SIGNING_SECRET) {
  throw new Error("SLACK_SIGNING_SECRET is required.");
}

const awsLambdaReceiver = new AwsLambdaReceiver({
  signingSecret: SLACK_SIGNING_SECRET,
});

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  receiver: awsLambdaReceiver,
});

HelloController(app);

type AwsHandler = Awaited<ReturnType<AwsLambdaReceiver["start"]>>;

export const handler: AwsHandler = async (event, context, callback) => {
  const handler = await awsLambdaReceiver.start();
  return handler(event, context, callback);
};
