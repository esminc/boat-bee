import { LambdaIntegration, RestApi } from "aws-cdk-lib/aws-apigateway";
import { AttributeType, Table } from "aws-cdk-lib/aws-dynamodb";
import { Runtime, Function, Code, Handler } from "aws-cdk-lib/aws-lambda";
import { LambdaDestination } from "aws-cdk-lib/aws-logs-destinations";
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
import { Rule, Schedule } from "aws-cdk-lib/aws-events";
import {
  LambdaFunction,
  SfnStateMachine,
} from "aws-cdk-lib/aws-events-targets";
import {
  Choice,
  StateMachine,
  Condition,
  Wait,
  WaitTime,
} from "aws-cdk-lib/aws-stepfunctions";
import { LambdaInvoke } from "aws-cdk-lib/aws-stepfunctions-tasks";

interface Props extends StackProps {
  stage: string;
  isProduction: boolean;
}

export class BeeSlackAppStack extends Stack {
  constructor(scope: Construct, id: string, props: Props) {
    super(scope, id, props);

    const { stage, isProduction } = props;

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
      pointInTimeRecovery: true,
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

    const targetBucketOfDynamoDBExport = new s3.Bucket(
      this,
      "TargetBucketOfDynamoDBExport",
      {
        removalPolicy,
        autoDeleteObjects: !isProduction,
      }
    );

    const exportDynamoDBTableToS3RequestFunction = new Function(
      this,
      "ExportDynamoDBTableToS3RequestLambda",
      {
        description: buildResourceDescription({
          resourceName: "ExportDynamoDBTableToS3RequestLambda",
          stage,
        }),
        runtime: Runtime.FROM_IMAGE,
        handler: Handler.FROM_IMAGE,
        code: Code.fromAssetImage(
          join(__dirname, "../../lambda/export_dynamodb_table_to_s3_request")
        ),
        environment: {
          DYNAMODB_TABLE_ARN: dynamoTable.tableArn,
          S3_BUCKET_NAME: targetBucketOfDynamoDBExport.bucketName,
        },
      }
    );

    exportDynamoDBTableToS3RequestFunction.addToRolePolicy(
      new PolicyStatement({
        actions: ["dynamodb:exportTableToPointInTime"],
        resources: [dynamoTable.tableArn],
      })
    );

    targetBucketOfDynamoDBExport.grantWrite(
      exportDynamoDBTableToS3RequestFunction
    );

    const exportDynamoDBTableToS3RequestLambdaTask = new LambdaInvoke(
      this,
      "ExportDynamoDBTableToS3RequestLambdaTask",
      { lambdaFunction: exportDynamoDBTableToS3RequestFunction }
    );

    const exportDynamoDBTableToS3CheckStatusFunction = new Function(
      this,
      "ExportDynamoDBTableToS3CheckStatusLambda",
      {
        description: buildResourceDescription({
          resourceName: "ExportDynamoDBTableToS3CheckStatusLambda",
          stage,
        }),
        runtime: Runtime.FROM_IMAGE,
        handler: Handler.FROM_IMAGE,
        code: Code.fromAssetImage(
          join(
            __dirname,
            "../../lambda/export_dynamodb_table_to_s3_check_status"
          )
        ),
      }
    );

    exportDynamoDBTableToS3CheckStatusFunction.addToRolePolicy(
      new PolicyStatement({
        actions: ["dynamodb:DescribeExport"],
        resources: ["*"],
      })
    );

    const exportDynamoDBTableToS3CheckStatusLambdaTask = new LambdaInvoke(
      this,
      "ExportDynamoDBTableToS3CheckStatusLambdaTask",
      {
        lambdaFunction: exportDynamoDBTableToS3CheckStatusFunction,
        outputPath: "$.Payload",
      }
    );

    const convertedDynamoDBJsonBucket = new s3.Bucket(
      this,
      "ConvertedDynamoDBJsonBucket",
      {
        removalPolicy,
        autoDeleteObjects: !isProduction,
      }
    );

    const exportDynamoDBTableToS3ConvertFunction = new Function(
      this,
      "ExportDynamoDBTableToS3ConvertLambda",
      {
        description: buildResourceDescription({
          resourceName: "ExportDynamoDBTableToS3ConvertLambda",
          stage,
        }),
        runtime: Runtime.FROM_IMAGE,
        handler: Handler.FROM_IMAGE,
        environment: {
          DYNAMODB_EXPORT_BUCKET: targetBucketOfDynamoDBExport.bucketName,
          CONVERTED_DYNAMODB_JSON_BUCKET:
            convertedDynamoDBJsonBucket.bucketName,
        },
        code: Code.fromAssetImage(
          join(__dirname, "../../lambda/export_dynamodb_table_to_s3_convert")
        ),
        timeout: Duration.minutes(3),
        memorySize: 1024,
      }
    );

    targetBucketOfDynamoDBExport.grantRead(
      exportDynamoDBTableToS3ConvertFunction
    );
    convertedDynamoDBJsonBucket.grantWrite(
      exportDynamoDBTableToS3ConvertFunction
    );

    const exportDynamoDBTableToS3ConvertLambdaTask = new LambdaInvoke(
      this,
      "ExportDynamoDBTableToS3ConvertLambdaTask",
      {
        lambdaFunction: exportDynamoDBTableToS3ConvertFunction,
      }
    );

    const exportDynamoDBWait = new Wait(this, "Wait for export", {
      time: WaitTime.duration(Duration.minutes(10)),
    });

    const exportDynamoDBChoice = new Choice(this, "Export complete?")
      .when(
        Condition.not(Condition.stringEquals("$.exportStatus", "IN_PROGRESS")),
        exportDynamoDBTableToS3ConvertLambdaTask
      )
      .otherwise(exportDynamoDBWait);

    const definition = exportDynamoDBTableToS3RequestLambdaTask
      .next(exportDynamoDBWait)
      .next(exportDynamoDBTableToS3CheckStatusLambdaTask)
      .next(exportDynamoDBChoice);

    const dynamoDBTableExportStateMachine = new StateMachine(
      this,
      "DynamoDBTableExportStateMachine",
      { definition }
    );

    new Rule(this, "DynamoDBTableExportRule", {
      description: buildResourceDescription({
        resourceName: "DynamoDBTableExportRule",
        stage,
      }),
      schedule: Schedule.cron({ hour: "23", minute: "0" }), // 毎日08:00(JST)に実行
      targets: [new SfnStateMachine(dynamoDBTableExportStateMachine)],
    });

    const secret = new Secret(this, "Secret", {
      description: buildResourceDescription({
        resourceName: "Secret",
        stage,
      }),
      removalPolicy,
      // デプロイ後に実際の値を手動で設定すること
      secretObjectValue: {
        SLACK_APP_TOKEN: SecretValue.unsafePlainText("dummy"),
        SLACK_BOT_TOKEN: SecretValue.unsafePlainText("dummy"),
        SLACK_SIGNING_SECRET: SecretValue.unsafePlainText("dummy"),
        NOTIFY_POST_REVIEW_CHANNEL: SecretValue.unsafePlainText("dummy"),
        BEE_OPERATION_BOT_SLACK_WEBHOOK_URL:
          SecretValue.unsafePlainText("dummy"),
        BEE_OPERATION_BOT_SLACK_BOT_TOKEN: SecretValue.unsafePlainText("dummy"),
        BEE_OPERATION_BOT_SLACK_CHANNEL: SecretValue.unsafePlainText("dummy"),
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

    const appFunction = new Function(this, "AppLambda", {
      description: buildResourceDescription({
        resourceName: "AppLambda",
        stage,
      }),
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

    const api = new RestApi(this, "RestAPI", {
      description: buildResourceDescription({
        resourceName: "RestAPI",
        stage,
      }),
    });

    api.root
      .addResource("slack")
      .addResource("events")
      .addMethod("POST", new LambdaIntegration(appFunction));

    const errorHandlerFunction = new Function(this, "ErrorHandlerLambda", {
      description: buildResourceDescription({
        resourceName: "ErrorHandlerLambda",
        stage,
      }),
      runtime: Runtime.FROM_IMAGE,
      handler: Handler.FROM_IMAGE,
      code: Code.fromAssetImage(join(__dirname, "../../lambda/error_handler")),
      environment: {
        SLACK_CREDENTIALS_SECRET_ID: secret.secretName,
      },
      timeout: Duration.minutes(3),
      memorySize: 1024,
    });

    secret.grantRead(errorHandlerFunction);

    appFunction.logGroup.addSubscriptionFilter("ErrorSubscriptionFilter", {
      destination: new LambdaDestination(errorHandlerFunction),
      filterPattern: { logPatternString: "ERROR" },
    });

    const bookRecommendationFunction = new Function(
      this,
      "BookRecommendationLambda",
      {
        description: buildResourceDescription({
          resourceName: "BookRecommendationLambda",
          stage,
        }),
        runtime: Runtime.FROM_IMAGE,
        handler: Handler.FROM_IMAGE,
        code: Code.fromAssetImage(
          join(__dirname, "../../lambda/book_recommendation")
        ),
        environment: {
          DYNAMODB_TABLE: dynamoTable.tableName,
        },
        timeout: Duration.minutes(3),
        memorySize: 1024,
      }
    );

    dynamoTable.grantReadWriteData(bookRecommendationFunction);

    new Rule(this, "BookRecommendationRule", {
      description: buildResourceDescription({
        resourceName: "BookRecommendationRule",
        stage,
      }),
      schedule: Schedule.cron({ hour: "0", minute: "0" }), // 毎日09:00(JST)に実行
      targets: [new LambdaFunction(bookRecommendationFunction)],
    });

    const reportFunction = new Function(this, "ReportLambda", {
      description: buildResourceDescription({
        resourceName: "ReportLambda",
        stage,
      }),
      runtime: Runtime.FROM_IMAGE,
      handler: Handler.FROM_IMAGE,
      code: Code.fromAssetImage(join(__dirname, "../../lambda/report")),
      environment: {
        SLACK_CREDENTIALS_SECRET_ID: secret.secretName,
        CONVERTED_DYNAMODB_JSON_BUCKET: convertedDynamoDBJsonBucket.bucketName,
      },
      timeout: Duration.minutes(3),
      memorySize: 1024,
    });

    convertedDynamoDBJsonBucket.grantRead(reportFunction);
    secret.grantRead(reportFunction);

    new Rule(this, "ReportRule", {
      description: buildResourceDescription({
        resourceName: "ReportRule",
        stage,
      }),
      schedule: Schedule.cron({ weekDay: "MON", hour: "0", minute: "0" }), // 毎週月曜日09:00(JST)に実行
      targets: [new LambdaFunction(reportFunction)],
    });

    const reportReviewGraphFunction = new Function(
      this,
      "ReportReviewGraphLambda",
      {
        description: buildResourceDescription({
          resourceName: "ReportReviewGraphLambda",
          stage,
        }),
        runtime: Runtime.FROM_IMAGE,
        handler: Handler.FROM_IMAGE,
        code: Code.fromAssetImage(
          join(__dirname, "../../lambda/report_review_graph")
        ),
        environment: {
          SLACK_CREDENTIALS_SECRET_ID: secret.secretName,
          CONVERTED_DYNAMODB_JSON_BUCKET:
            convertedDynamoDBJsonBucket.bucketName,
        },
        timeout: Duration.minutes(3),
        memorySize: 1024,
      }
    );

    convertedDynamoDBJsonBucket.grantRead(reportReviewGraphFunction);
    secret.grantRead(reportReviewGraphFunction);

    new Rule(this, "ReportReviewGraphRule", {
      description: buildResourceDescription({
        resourceName: "ReportReviewGraphRule",
        stage,
      }),
      schedule: Schedule.cron({ weekDay: "MON", hour: "0", minute: "0" }), // 毎週月曜日09:00(JST)に実行
      targets: [new LambdaFunction(reportReviewGraphFunction)],
    });

    const reportUserActionGraphFunction = new Function(
      this,
      "ReportUserActionGraphLambda",
      {
        description: buildResourceDescription({
          resourceName: "ReportUserActionGraphLambda",
          stage,
        }),
        runtime: Runtime.FROM_IMAGE,
        handler: Handler.FROM_IMAGE,
        code: Code.fromAssetImage(
          join(__dirname, "../../lambda/report_user_action_graph")
        ),
        environment: {
          SLACK_CREDENTIALS_SECRET_ID: secret.secretName,
          CONVERTED_DYNAMODB_JSON_BUCKET:
            convertedDynamoDBJsonBucket.bucketName,
        },
        timeout: Duration.minutes(3),
        memorySize: 1024,
      }
    );

    convertedDynamoDBJsonBucket.grantRead(reportUserActionGraphFunction);
    secret.grantRead(reportUserActionGraphFunction);

    new Rule(this, "ReportUserActionGraphRule", {
      description: buildResourceDescription({
        resourceName: "ReportUserActionGraphRule",
        stage,
      }),
      schedule: Schedule.cron({ weekDay: "MON", hour: "0", minute: "0" }), // 毎週月曜日09:00(JST)に実行
      targets: [new LambdaFunction(reportUserActionGraphFunction)],
    });
  }
}

const buildResourceDescription = (props: {
  resourceName: string;
  stage: string;
}) => {
  return `${props.resourceName} : ${props.stage}`;
};
