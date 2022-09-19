import { Axios } from "axios";

const GOOGLE_BOOKS_API_ENDPOINT = "https://www.googleapis.com/books/v1/volumes";

const client = new Axios();

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
    const { data } = await client.get(GOOGLE_BOOKS_API_ENDPOINT, {
      params: {
        q: `intitle:${title}`,
        Country: "JP",
      },
    });

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
