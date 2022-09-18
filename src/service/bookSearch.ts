import { SearchedBook } from "../model";
import { GoogleBooksRepository } from "../repository";

const googleBooksRepository = new GoogleBooksRepository();

class BookSearchService {
  /**
   * タイトルから書籍を検索する
   */
  async fetchByTitle(title: string): Promise<SearchedBook[] | undefined> {
    const books = await googleBooksRepository.searchBookByTitle(title);

    if (!books) {
      return undefined;
    }

    return books.map((book) => {
      return {
        title: book.title,
        isbn: book.isbn,
        authors: book.authors,
        imageUrl: book.imageUrl,
        googleBooksUrl: book.googleBooksUrl,
        description: book.description,
      };
    });
  }

  /**
   * ISBNから書籍を検索する
   */
  async fetchByIsbn(isbn: string): Promise<SearchedBook | undefined> {
    const book = await googleBooksRepository.searchBookByIsbn(isbn);

    if (!book) {
      return undefined;
    }

    return {
      title: book.title,
      isbn: book.isbn,
      authors: book.authors,
      imageUrl: book.imageUrl,
      googleBooksUrl: book.googleBooksUrl,
      description: book.description,
    };
  }
}

export { BookSearchService };
