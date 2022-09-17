import { App, AwsLambdaReceiver } from "@slack/bolt";
import { HelloController } from "./view_controller";

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
