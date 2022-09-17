import { User, Pagination } from "../model";
import { PutItemCommand } from "@aws-sdk/client-dynamodb";
import { dynamoDBClient } from "./database";

const TABLE_NAME = "bee-dev";

class UserRepository {
  private GSI_PK_VALUE = "user" as const;

  /**
   * ユーザを追加・更新する
   */
  async put(user: User): Promise<void> {
    const partitionKey = this.encodePartitionKey(user["user_id"]);

    const command = new PutItemCommand({
      TableName: TABLE_NAME,
      Item: {
        PK: { S: partitionKey },
        GSI_PK: { S: this.GSI_PK_VALUE },
        GSI_0_SK: { S: user["updated_at"] || "" },
        GSI_3_SK: { N: String(user["post_review_count"]) },
        user_id: { S: user["user_id"] },
        user_name: { S: user["user_name"] },
        department: { S: user["department"] },
        job_type: { S: user["job_type"] },
        age_range: { S: user["age_range"] },
        updated_at: { S: user["updated_at"] || "" },
        post_review_count: { N: String(user["post_review_count"]) },
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
  async fetch(isbn: string): Promise<User | null> {
    return null;
  }

  /**
   * 全てのユーザー情報を取得する
   */
  async fetchByUserId(userId: string): Promise<User[] | null> {
    return null;
  }

  /**
   * レビューを投稿しているユーザを取得する
   */
  async fetchByPostedReview(userId: string): Promise<Pagination<User> | null> {
    return null;
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
