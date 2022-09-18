const GOOGLE_BOOKS_API_ENDPOINT = "https://www.googleapis.com/books/v1/volumes";

class GoogleBooksRepository {
  /**
   * タイトルから書籍を検索する
   */
  async searchBookByTitle(title: string): Promise<
    | {
        title: string;
        isbn: string;
        authors: string[];
        imageUrl: string;
        googleBooksUrl: string;
        description: string;
      }[]
    | undefined
  > {
    return undefined;
  }

  /**
   * ISBNから書籍を検索する
   */
  async searchBookByIsbn(isbn: string): Promise<
    | {
        title: string;
        isbn: string;
        authors: string[];
        imageUrl: string;
        googleBooksUrl: string;
        description: string;
      }
    | undefined
  > {
    return undefined;
  }
}

export { GoogleBooksRepository };
