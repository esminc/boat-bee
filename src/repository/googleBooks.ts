const GOOGLE_BOOKS_API_ENDPOINT = "https://www.googleapis.com/books/v1/volumes";

class GoogleBooksRepository {
  /**
   * タイトルから書籍を検索する
   */
  async searchBookByTitle(isbn: string) {
    return null;
  }

  /**
   * ISBNから書籍を検索する
   */
  async searchBookByIsbn(userId: string) {
    return null;
  }
}

export { GoogleBooksRepository };
