import { UserAction } from "../model";
import { PutItemCommand } from "@aws-sdk/client-dynamodb";
import { dynamoDBClient } from "./database";

const TABLE_NAME = "bee-dev";

class UserActionRepository {
  /**
   * ユーザの行動履歴を追加する
   */
  async put(userAction: UserAction): Promise<void> {}
}

export { UserActionRepository };
