#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { BeeSlackAppStack } from "../lib/bee-slack-app-stack";

const stage = process.env.STAGE || "dev";

if (stage !== "dev" && stage !== "prod") {
  throw new Error("stage value is not supported.");
}

const app = new cdk.App();

new BeeSlackAppStack(app, `BeeSlackAppStack-${stage}`, {
  isProduction: stage === "prod",
});
