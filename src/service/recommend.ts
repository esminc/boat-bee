import { RecommendBook, SuggestedBook } from "../model";
import { now } from "../utils/datetime";
import {
  RecommendBooksRepository,
  BookRepository,
  SuggestedBooksRepository,
} from "../repository";

const recommendBooksRepository = new RecommendBooksRepository();
const booksRepository = new BookRepository();
const suggestedBooksRepository = new SuggestedBooksRepository();

class RecommendService {
  /**
   * おすすめの本を取得する
   */
  async fetch(userId: string): Promise<RecommendBook[] | undefined> {
    const recommendBookAndMlModel = await recommendBooksRepository.fetch(
      userId
    );

    if (!recommendBookAndMlModel) {
      return undefined;
    }

    const recommendBooks: RecommendBook[] = [];

    Object.entries(recommendBookAndMlModel).forEach(async (recommendBook) => {
      const mlModel = recommendBook[0];
      const isbn = recommendBook[1];

      const book = await booksRepository.fetch(isbn);

      if (book) {
        const suggestedBook = await suggestedBooksRepository.fetch({
          userId,
          isbn,
          mlModel,
        });

        if (!suggestedBook) {
          // おすすめ本が未登録の場合はそれを登録する
          await suggestedBooksRepository.put({
            userId,
            isbn,
            mlModel,
            interested: false,
            updatedAt: now(),
          });
        }

        const interested = suggestedBook ? suggestedBook.interested : false;

        recommendBooks.push({
          title: book.title,
          isbn,
          author: book.author,
          url: book.url,
          imageUrl: book.imageUrl,
          description: book.description,
          updatedAt: book.updatedAt,
          interested,
          mlModel,
        });
      }
    });

    return recommendBooks;
  }

  /**
   * おすすめ情報の生成時刻をISO 8601形式で取得する
   *
   * YYYY/mm/dd HH:MM:SSの時刻文字列。例 2022/04/01 00:00:00
   */
  async getCreatedAt(): Promise<string | undefined> {
    const metadata = await recommendBooksRepository.fetchMetadata();

    return metadata ? metadata.createdAt : undefined;
  }

  /**
   * おすすめされた本の情報（履歴）を登録・更新する
   */
  async updateSuggestedBookState(suggestedBook: SuggestedBook): Promise<void> {
    await suggestedBooksRepository.put({ ...suggestedBook, updatedAt: now() });
  }
}

export { RecommendService };
