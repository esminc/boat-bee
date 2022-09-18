import { Book, validateBook } from "../model";
import { GetResponse } from "./types";
import { QueryCommand, QueryCommandInput } from "@aws-sdk/client-dynamodb";
import { dynamoDBClient } from "./database";

async function query(
  otherInput: QueryCommandInput;
  tableName: string,
  exclusiveStartKey?: any,
  maxItemCount?: number
) {
  const command = new QueryCommand({
    ...otherInput,
    TableName: tableName,
    Limit: maxItemCount,
    ExclusiveStartKey: exclusiveStartKey,
  });

  const { Items, LastEvaluatedKey } = await dynamoDBClient.send(command);

  return { Items, LastEvaluatedKey };
}

const TABLE_NAME = "bee-dev";
class BookRepository {
  private GSI_PK_VALUE = "book" as const;

  /**
   * レビューが投稿されている本を保存する
   */
  async put(book: Book): Promise<Book | undefined> {
    return undefined;
  }

  /**
   * レビューが投稿されている本を取得する
   */
  async fetch(isbn: string): Promise<Book | undefined> {
    return undefined;
  }

  /**
   * レビューが投稿されている本のリストを取得する
   */
  async fetchAll(params: {
    limit?: number;
    startKey?: any;
  }): Promise<GetResponse<Book> | undefined> {
    const command = new QueryCommand({
      TableName: TABLE_NAME,
      ExpressionAttributeNames: { "#attr": "GSI_PK" },
      ExpressionAttributeValues: { ":val": { S: this.GSI_PK_VALUE } },
      KeyConditionExpression: "#attr = :val",
    });

    try {
      const { Items, LastEvaluatedKey } = await dynamoDBClient.send(command);

      if (!Items) {
        return undefined;
      }

      const items = Items.map((Item) => {
        const book = {
          isbn: Item.isbn.S,
          title: Item.title.S,
          author: Item.author.S,
          url: Item.url.S,
          imageUrl: Item.imageUrl.S,
          description: Item.description.S,
          updatedAt: Item.updatedAt.S,
        };

        return validateBook(book);
      });

      return { items, lastKey: LastEvaluatedKey };
    } catch (error) {
      console.error(error);
    }
  }

  private encodePartitionKey(isbn: string) {
    return `book#${isbn}`;
  }
}

export { BookRepository };
