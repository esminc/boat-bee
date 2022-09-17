import { SearchedBook } from "../model";

class BookSearchService {
  /**
   * タイトルから書籍を検索する
   */
  async fetchByTitle(title: string): Promise<SearchedBook[] | null> {
    return null;
  }

  /**
   * ISBNから書籍を検索する
   */
  async fetchByIsbn(isbn: string): Promise<SearchedBook | null> {
    return null;
  }
}

export { BookSearchService };
