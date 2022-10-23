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
import * as s3 from "aws-cdk-lib/aws-s3";
import * as cloudfront from "aws-cdk-lib/aws-cloudfront";
import * as s3deploy from "aws-cdk-lib/aws-s3-deployment";
import * as cloudfront_origins from "aws-cdk-lib/aws-cloudfront-origins";
import { PolicyStatement, CanonicalUserPrincipal } from "aws-cdk-lib/aws-iam";

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

    const cloudfrontOAI = new cloudfront.OriginAccessIdentity(
      this,
      "cloudfront-OAI"
    );

    const assetBucket = new s3.Bucket(this, "AssetBucket", {
      removalPolicy,
      autoDeleteObjects: !isProduction,
    });

    assetBucket.addToResourcePolicy(
      new PolicyStatement({
        actions: ["s3:GetObject"],
        resources: [assetBucket.arnForObjects("*")],
        principals: [
          new CanonicalUserPrincipal(
            cloudfrontOAI.cloudFrontOriginAccessIdentityS3CanonicalUserId
          ),
        ],
      })
    );

    const distribution = new cloudfront.Distribution(
      this,
      "AssetDistribution",
      {
        minimumProtocolVersion: cloudfront.SecurityPolicyProtocol.TLS_V1_2_2021,
        defaultBehavior: {
          origin: new cloudfront_origins.S3Origin(assetBucket, {
            originAccessIdentity: cloudfrontOAI,
          }),
          compress: true,
          allowedMethods: cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
          viewerProtocolPolicy:
            cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        },
      }
    );

    new s3deploy.BucketDeployment(this, "AssetDeployment", {
      sources: [s3deploy.Source.asset("../assets")],
      destinationBucket: assetBucket,
      distribution,
      distributionPaths: ["/*"],
    });

    const appFunction = new Function(this, "Lambda", {
      runtime: Runtime.FROM_IMAGE,
      handler: Handler.FROM_IMAGE,
      code: Code.fromAssetImage(join(__dirname, "../../lambda/app")),
      environment: {
        SLACK_CREDENTIALS_SECRET_ID: secret.secretName,
        DYNAMODB_TABLE: dynamoTable.tableName,
        ASSET_URL: "https://" + distribution.distributionDomainName,
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
