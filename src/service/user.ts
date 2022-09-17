import { User } from "../model";

class UserService {
  /**
   * ユーザを取得する
   */
  async fetch(userId: string): Promise<User | null> {}
}

export { UserService };
