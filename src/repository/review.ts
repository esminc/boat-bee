import { Review, Pagination } from "../model";
import { PutItemCommand } from "@aws-sdk/client-dynamodb";
import { dynamoDBClient } from "./database";

const TABLE_NAME = "bee-dev";

class ReviewRepository {
  private GSI_PK_VALUE = "review" as const;

  /**
   * レビューを追加・更新する
   */
  async put(review: Review): Promise<Review | undefined> {
    const partitionKey = this.encodePartitionKey(review.userId, review.isbn);

    const command = new PutItemCommand({
      TableName: TABLE_NAME,
      Item: {
        PK: { S: partitionKey },
        GSI_PK: { S: this.GSI_PK_VALUE },
        GSI_0_SK: { S: review.updatedAt || "" },
        GSI_1_SK: { S: review.userId },
        GSI_2_SK: { S: review["isbn"] },
        user_id: { S: review.userId },
        book_title: { S: review.bookTitle },
        isbn: { S: review["isbn"] },
        score_for_me: { S: review.scoreForMe },
        score_for_others: { S: review.scoreForOthers },
        review_comment: { S: review.reviewComment },
        updated_at: { S: review.updatedAt || "" },
        book_image_url: { S: review.bookImageUrl },
        book_author: { S: review.bookAuthor },
        book_url: { S: review.bookUrl },
        book_description: { S: review.bookDescription },
      },
    });

    try {
      await dynamoDBClient.send(command);

      return review;
    } catch (error) {
      console.error(error);
    }
  }

  /**
   * 本のレビューを取得する
   */
  async fetch(userId: string, isbn: string): Promise<Review | undefined> {
    return undefined;
  }

  /**
   * ユーザIDから、本のレビューを取得する
   */
  async fetchByUserId(userId: string): Promise<Review[] | undefined> {
    return undefined;
  }

  /**
   * ユーザIDから、本のレビューを取得する(ページネーション対応)
   */
  async fetchByUserIdWithPagination(
    userId: string
  ): Promise<Pagination<Review> | undefined> {
    return undefined;
  }

  /**
   * ISBNから、本のレビューを取得する
   */
  async fetchByIsbn(isbn: string): Promise<Review | undefined> {
    return undefined;
  }

  /**
   * 全ての本のレビューを取得する
   */
  async fetchAll(): Promise<Review[] | undefined> {
    return undefined;
  }

  private encodePartitionKey(userId: string, isbn: string) {
    return `review#${userId}#${isbn}`;
  }
}

export { ReviewRepository };
