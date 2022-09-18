import { SuggestedBook } from "../model";

class SuggestedBooksRepository {
  /**
   * おすすめされた本を追加・更新する
   */
  async put(suggestedBook: SuggestedBook): Promise<void> {
    return undefined;
  }

  /**
   * おすすめされた本を取得する
   */
  async fetch(params: {
    userId: string;
    isbn: string;
    mlModel: string;
  }): Promise<SuggestedBook | undefined> {
    return undefined;
  }
}

export { SuggestedBooksRepository };
