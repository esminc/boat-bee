import { User } from "../model";

class UserService {
  /**
   * ユーザを追加・更新する
   */
  async put(user: User): Promise<void> {}

  /**
   * ユーザを取得する
   */
  async fetch(userId: string): Promise<User | undefined> {
    return undefined;
  }

  /**
   * 全てのユーザを取得する
   */
  async fetchAll(): Promise<User[] | undefined> {
    return undefined;
  }

  /**
   * レビューを投稿しているユーザを取得する
   */
  async fetchByPostedReview(): Promise<User[] | undefined> {
    return undefined;
  }
}

export { UserService };
