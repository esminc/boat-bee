import { Book, validateBook } from "../model";
import { GetResponse } from "./types";
import { QueryCommand, QueryCommandInput } from "@aws-sdk/client-dynamodb";
import { dynamoDBClient } from "./database";

async function query(params: {
  tableName: string;
  exclusiveStartKey?: any;
  maxItemCount?: number;
  otherInput?: Partial<QueryCommandInput>;
}) {
  const command = new QueryCommand({
    ...params.otherInput,
    TableName: params.tableName,
    Limit: params.maxItemCount,
    ExclusiveStartKey: params.exclusiveStartKey,
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
    try {
      let lastEvaluatedKey = undefined;
      let items = undefined;

      let queryResult = await query({
        tableName: TABLE_NAME,
        maxItemCount: params.limit,
        otherInput: {
          IndexName: "GSI_0",
          ExpressionAttributeNames: { "#attr": "GSI_PK" },
          ExpressionAttributeValues: { ":val": { S: this.GSI_PK_VALUE } },
          KeyConditionExpression: "#attr = :val",
        },
      });

      items = queryResult.Items;
      lastEvaluatedKey = queryResult.LastEvaluatedKey;

      if (!items) {
        return undefined;
      }

      if (!params.limit) {
        while (lastEvaluatedKey) {
          queryResult = await query({
            tableName: TABLE_NAME,
            exclusiveStartKey: lastEvaluatedKey,
            otherInput: {
              IndexName: "GSI_0",
              ExpressionAttributeNames: { "#attr": "GSI_PK" },
              ExpressionAttributeValues: { ":val": { S: this.GSI_PK_VALUE } },
              KeyConditionExpression: "#attr = :val",
            },
          });

          if (queryResult.Items) {
            items.concat(queryResult.Items);
          }
          lastEvaluatedKey = queryResult.LastEvaluatedKey;
        }
      }

      return {
        items: items.map((Item) => {
          const book = {
            isbn: Item.isbn.S,
            title: Item.title.S,
            author: Item.author.S,
            url: Item.url.S,
            imageUrl: Item.image_url.S,
            description: Item.description.S,
            updatedAt: Item.updated_at.S,
          };

          return validateBook(book);
        }),
        lastKey: lastEvaluatedKey,
      };
    } catch (error) {
      console.error(error);
    }
  }

  private encodePartitionKey(isbn: string) {
    return `book#${isbn}`;
  }
}

export { BookRepository };
