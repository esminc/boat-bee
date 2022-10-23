import { LambdaIntegration, RestApi } from "aws-cdk-lib/aws-apigateway";
import { AttributeType, Table } from "aws-cdk-lib/aws-dynamodb";
import { Runtime, Function, Code, Handler } from "aws-cdk-lib/aws-lambda";
import {
  StackProps,
  Stack,
  RemovalPolicy,
  SecretValue,
  Duration,
} from "aws-cdk-lib";
import { Secret } from "aws-cdk-lib/aws-secretsmanager";
import { Construct } from "constructs";
import { join } from "path";

interface Props extends StackProps {
  isProduction: boolean;
}

export class BeeSlackAppStack extends Stack {
  constructor(scope: Construct, id: string, props: Props) {
    super(scope, id, props);

    const isProduction = props.isProduction;

    const removalPolicy = isProduction
      ? RemovalPolicy.RETAIN
      : RemovalPolicy.DESTROY;

    const dynamoTable = new Table(this, "DynamoDBTable", {
      partitionKey: {
        name: "PK",
        type: AttributeType.STRING,
      },
      readCapacity: 1,
      writeCapacity: 1,
      removalPolicy,
      pointInTimeRecovery: isProduction,
    });

    dynamoTable.addGlobalSecondaryIndex({
      indexName: "GSI_0",
      partitionKey: {
        name: "GSI_PK",
        type: AttributeType.STRING,
      },
      sortKey: {
        name: "GSI_0_SK",
        type: AttributeType.STRING,
      },
    });
    dynamoTable.addGlobalSecondaryIndex({
      indexName: "GSI_1",
      partitionKey: {
        name: "GSI_PK",
        type: AttributeType.STRING,
      },
      sortKey: {
        name: "GSI_1_SK",
        type: AttributeType.STRING,
      },
    });
    dynamoTable.addGlobalSecondaryIndex({
      indexName: "GSI_2",
      partitionKey: {
        name: "GSI_PK",
        type: AttributeType.STRING,
      },
      sortKey: {
        name: "GSI_2_SK",
        type: AttributeType.STRING,
      },
    });
    dynamoTable.addGlobalSecondaryIndex({
      indexName: "GSI_3",
      partitionKey: {
        name: "GSI_PK",
        type: AttributeType.STRING,
      },
      sortKey: {
        name: "GSI_3_SK",
        type: AttributeType.NUMBER,
      },
    });

    const secret = new Secret(this, "Secret", {
      removalPolicy,
      // デプロイ後に実際の値を手動で設定すること
      secretObjectValue: {
        SLACK_APP_TOKEN: SecretValue.unsafePlainText("dummy"),
        SLACK_BOT_TOKEN: SecretValue.unsafePlainText("dummy"),
        SLACK_SIGNING_SECRET: SecretValue.unsafePlainText("dummy"),
        NOTIFY_POST_REVIEW_CHANNEL: SecretValue.unsafePlainText("dummy"),
      },
    });

    const appFunction = new Function(this, "Lambda", {
      runtime: Runtime.FROM_IMAGE,
      handler: Handler.FROM_IMAGE,
      code: Code.fromAssetImage(join(__dirname, "../../lambda/app")),
      environment: {
        SLACK_CREDENTIALS_SECRET_ID: secret.secretName,
        DYNAMODB_TABLE: dynamoTable.tableName,
      },
      timeout: Duration.minutes(3),
      memorySize: 1024,
    });

    dynamoTable.grantReadWriteData(appFunction);
    secret.grantRead(appFunction);

    const api = new RestApi(this, "RestAPI");

    api.root
      .addResource("slack")
      .addResource("events")
      .addMethod("POST", new LambdaIntegration(appFunction));
  }
}
