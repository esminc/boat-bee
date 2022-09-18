import { RecommendBook } from "../model";

class RecommendService {
  /**
   * おすすめの本を取得する
   */
  async fetch(userId: string): Promise<RecommendBook[] | undefined> {
    return undefined;
  }

  /**
   * おすすめ情報の生成時刻をISO 8601形式で取得する
   *
   * YYYY/mm/dd HH:MM:SSの時刻文字列。例 2022/04/01 00:00:00
   */
  async getCreatedAt(): Promise<string | undefined> {
    return undefined;
  }

  /**
   * おすすめされた本の情報（履歴）を登録・更新する
   */
  async updateSuggestedBookState(): Promise<void> {}
}

export { RecommendService };
