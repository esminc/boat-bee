import { Review, Pagination } from "../model";
import { PutItemCommand } from "@aws-sdk/client-dynamodb";
import { dynamoDBClient } from "./database";

const TABLE_NAME = "bee-dev";

class ReviewRepository {
  private GSI_PK_VALUE = "review" as const;

  /**
   * レビューを追加・更新する
   */
  async put(review: Review): Promise<Review | null> {
    const partitionKey = this.encodePartitionKey(
      review["user_id"],
      review["isbn"]
    );

    const command = new PutItemCommand({
      TableName: TABLE_NAME,
      Item: {
        PK: { S: partitionKey },
        GSI_PK: { S: this.GSI_PK_VALUE },
        GSI_0_SK: { S: review["updated_at"] || "" },
        GSI_1_SK: { S: review["user_id"] },
        GSI_2_SK: { S: review["isbn"] },
        user_id: { S: review["user_id"] },
        book_title: { S: review["book_title"] },
        isbn: { S: review["isbn"] },
        score_for_me: { S: review["score_for_me"] },
        score_for_others: { S: review["score_for_others"] },
        review_comment: { S: review["review_comment"] },
        updated_at: { S: review["updated_at"] || "" },
        book_image_url: { S: review["book_image_url"] },
        book_author: { S: review["book_author"] },
        book_url: { S: review["book_url"] },
        book_description: { S: review["book_description"] },
      },
    });

    try {
      await dynamoDBClient.send(command);
    } catch (error) {
      console.error(error);
    }
  }

  /**
   * 本のレビューを取得する
   */
  async fetch(userId: string, isbn: string): Promise<Review | null> {
    return null;
  }

  /**
   * ユーザIDから、本のレビューを取得する
   */
  async fetchByUserId(userId: string): Promise<Review[] | null> {
    return null;
  }

  /**
   * ユーザIDから、本のレビューを取得する(ページネーション対応)
   */
  async fetchByUserIdWithPagination(
    userId: string
  ): Promise<Pagination<Review> | null> {
    return null;
  }

  /**
   * ISBNから、本のレビューを取得する
   */
  async fetchByIsbn(isbn: string): Promise<Review | null> {
    return null;
  }

  /**
   * 全ての本のレビューを取得する
   */
  async fetchAll(): Promise<Review[] | null> {
    return null;
  }

  private encodePartitionKey(userId: string, isbn: string) {
    return `review#${userId}#${isbn}`;
  }
}

export { ReviewRepository };
