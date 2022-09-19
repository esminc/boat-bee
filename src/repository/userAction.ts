import { UserAction } from "../model";
import { PutItemCommand } from "@aws-sdk/client-dynamodb";
import { dynamoDBClient } from "./database";

const TABLE_NAME = "bee-dev";
class UserActionRepository {
  private GSI_PK_VALUE = "user_action" as const;

  /**
   * ユーザの行動履歴を追加する
   */
  async put(userAction: UserAction): Promise<void> {
    try {
      const partitionKey = this.encodePartitionKey(
        userAction.userId,
        userAction.createdAt
      );

      const command = new PutItemCommand({
        TableName: TABLE_NAME,
        Item: {
          PK: { S: partitionKey },
          GSI_PK: { S: this.GSI_PK_VALUE },
          GSI_0_SK: { S: userAction.createdAt || "" },
          GSI_1_SK: { S: userAction.userId },
          user_id: { S: userAction.userId },
          created_at: { S: userAction.createdAt },
          action_name: { S: userAction.actionName },
          status: { S: userAction.status },
          payload: { S: userAction.payload },
        },
      });

      await dynamoDBClient.send(command);
    } catch (error) {
      console.error(error);
    }
  }

  private encodePartitionKey(userId: string, createdAt: string) {
    return `user_action#${userId}#${createdAt}`;
  }
}

export { UserActionRepository };
