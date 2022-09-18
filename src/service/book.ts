import { Book } from "../model";
import { BookRepository } from "../repository";

type Response<T> = { items: T[]; keys: any; hasNext: boolean };

type BeforeResponse<T> = { items: T[]; keys: any; isMoveToFirst: boolean };

const bookRepository = new BookRepository();

class BookService {
  /**
   * レビューが投稿されている本のリストを取得する
   */
  async fetch(params: {
    limit?: number;
    keys?: any[];
  }): Promise<Response<Book> | undefined> {
    const keys = params.keys || [];

    const startKey = keys.length > 0 ? keys[-1] : undefined;

    const books = await bookRepository.fetchAll({
      limit: params.limit,
      startKey,
    });

    if (!books) {
      return undefined;
    }

    console.log(books);

    const lastKey = books.lastKey || "end";

    return {
      items: books.items,
      keys: [...keys, lastKey],
      hasNext: lastKey !== "end",
    };
  }

  /**
   * レビューが投稿されている本のリストを取得する（前への移動）
   */
  async fetchBefore(userId: string): Promise<BeforeResponse<Book> | undefined> {
    return undefined;
  }
}

export { BookService };
