import { Review } from "../model";

class ReviewService {
  /**
   * レビューを取得する
   */
  async fetch(userId: string, isbn: string): Promise<Review | null> {}

  /**
   * 全てのレビューを取得する
   */
  async fetchAll(): Promise<Review[]> {}
}

export { ReviewService };
