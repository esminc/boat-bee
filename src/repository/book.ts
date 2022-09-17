type Book = {
  isbn: string;
  title: string;
  author: string;
  url: string;
  image_url: string;
  description: string;
  updated_at: string;
};

type BookItemKey = {};

class BookRepository {
  /**
   * レビューが投稿されている本を保存する
   */
  async put(entryId: number, userId: string): Promise<Book | null> {
    return null;
  }

  /**
   * レビューが投稿されている本を取得する
   */
  async fetch(isbn: string): Promise<Book | null> {
    return null;
  }

  /**
   * レビューが投稿されている本のリストを取得する
   */
  async fetchAll(limit?: number, startKey?: BookItemKey) {}
}

export { BookRepository };
