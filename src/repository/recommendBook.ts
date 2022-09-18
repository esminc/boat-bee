class RecommendBooksRepository {
  /**
   * おすすめの本を取得する
   */
  async fetch(userId: string): Promise<Record<string, string> | undefined> {
    return undefined;
  }

  /**
   * おすすめ情報のメタデータを取得する
   */
  async fetchMetadata(): Promise<{ createdAt: string } | undefined> {
    return undefined;
  }
}

export { RecommendBooksRepository };
