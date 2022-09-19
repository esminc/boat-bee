import { User } from "../model";
import { validateUser } from "../model/user.validator";
import {
  PutItemCommand,
  GetItemCommand,
  QueryCommand,
} from "@aws-sdk/client-dynamodb";
import { dynamoDBClient } from "./database";

const TABLE_NAME = "bee-dev";

class UserRepository {
  private GSI_PK_VALUE = "user" as const;

  /**
   * ユーザを追加・更新する
   */
  async put(user: User): Promise<void> {
    const partitionKey = this.encodePartitionKey(user.userId);

    const command = new PutItemCommand({
      TableName: TABLE_NAME,
      Item: {
        PK: { S: partitionKey },
        GSI_PK: { S: this.GSI_PK_VALUE },
        GSI_0_SK: { S: user.userId || "" },
        GSI_3_SK: { N: String(user.postReviewCount) },
        user_id: { S: user.userId },
        user_name: { S: user.userName },
        department: { S: user["department"] },
        job_type: { S: user.jobType },
        age_range: { S: user.ageRange },
        updated_at: { S: user.updatedAt || "" },
        post_review_count: { N: String(user.postReviewCount) },
      },
    });

    try {
      await dynamoDBClient.send(command);
    } catch (error) {
      console.error(error);
    }
  }

  /**
   * ユーザー情報を取得する
   */
  async fetch(userId: string): Promise<User | undefined> {
    const partitionKey = this.encodePartitionKey(userId);

    const command = new GetItemCommand({
      TableName: TABLE_NAME,
      Key: { PK: { S: partitionKey } },
    });

    try {
      const { Item } = await dynamoDBClient.send(command);

      if (!Item) {
        return undefined;
      }

      const user = {
        userId: Item.user_id.S,
        userName: Item.user_name.S,
        department: Item.department.S,
        jobType: Item.job_type.S,
        ageRange: Item.age_range.S,
        updatedAt: Item.updated_at.S,
        postReviewCount: Item.post_review_count.N,
      };

      return validateUser(user);
    } catch (error) {
      console.error(error);
    }
  }

  /**
   * 全てのユーザー情報を取得する
   */
  async fetchAll(): Promise<User[] | undefined> {
    const command = new QueryCommand({
      TableName: TABLE_NAME,
      IndexName: "GSI_0",
      ExpressionAttributeNames: { "#attr": "GSI_PK" },
      ExpressionAttributeValues: { ":val": { S: this.GSI_PK_VALUE } },
      KeyConditionExpression: "#attr = :val",
    });

    try {
      const { Items } = await dynamoDBClient.send(command);

      if (!Items) {
        return undefined;
      }

      return Items.map((Item) => {
        const user = {
          userId: Item.user_id.S,
          userName: Item.user_name.S,
          department: Item.department.S,
          jobType: Item.job_type.S,
          ageRange: Item.age_range.S,
          updatedAt: Item.updated_at.S,
          postReviewCount: Item.post_review_count.N,
        };

        return validateUser(user);
      });
    } catch (error) {
      console.error(error);
    }
  }

  /**
   * レビューを投稿しているユーザを取得する
   *
   * ユーザは、レビュー投稿数が多い順でソート済み
   */
  async fetchByPostedReview(): Promise<User[] | undefined> {
    try {
      const command = new QueryCommand({
        TableName: TABLE_NAME,
        IndexName: "GSI_3",
        ExpressionAttributeNames: { "#attr1": "GSI_PK", "#attr2": "GSI_3_SK" },
        ExpressionAttributeValues: {
          ":val1": { S: this.GSI_PK_VALUE },
          ":val2": { N: "0" },
        },
        KeyConditionExpression: "#attr1 = :val1 AND #attr2 >= :val2",
        ScanIndexForward: false,
      });

      const { Items } = await dynamoDBClient.send(command);

      if (!Items) {
        return undefined;
      }

      return Items.map((Item) => {
        const user = {
          userId: Item.user_id.S,
          userName: Item.user_name.S,
          department: Item.department.S,
          jobType: Item.job_type.S,
          ageRange: Item.age_range.S,
          updatedAt: Item.updated_at.S,
          postReviewCount: Number(Item.post_review_count.N),
        };

        return validateUser(user);
      });
    } catch (error) {
      console.error(error);
    }
  }

  /**
   * 投稿したレビューの数を更新する
   */
  async updatePostReviewCount(userId: string, count: number): Promise<void> {}

  private encodePartitionKey(userId: string) {
    return `user#${userId}`;
  }
}

export { UserRepository };
