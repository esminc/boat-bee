import { Book } from "../model";
import { GetResponse } from "./types";

class BookRepository {
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
  async fetchAll(
    limit?: number,
    startKey?: any
  ): Promise<GetResponse<Book> | undefined> {
    return undefined;
  }
}

export { BookRepository };
