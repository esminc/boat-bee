import { Book } from "../model";

type Response<T> = { items: T[]; keys: any; hasNext: boolean };

type BeforeResponse<T> = { items: T[]; keys: any; isMoveToFirst: boolean };

class BookService {
  /**
   * レビューが投稿されている本のリストを取得する
   */
  async fetch(userId: string): Promise<Response<Book> | null> {
    return null;
  }

  /**
   * レビューが投稿されている本のリストを取得する（前への移動）
   */
  async fetchBefore(userId: string): Promise<BeforeResponse<Book> | null> {
    return null;
  }
}

export { BookService };
