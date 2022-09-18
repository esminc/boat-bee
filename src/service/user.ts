import { User } from "../model";
import { UserRepository } from "../repository";

const userRepository = new UserRepository();

class UserService {
  /**
   * ユーザを追加・更新する
   */
  async put(user: User): Promise<void> {
    await userRepository.put(user);
  }

  /**
   * ユーザを取得する
   */
  async fetch(userId: string): Promise<User | undefined> {
    const user = await userRepository.fetch(userId);

    return user;
  }

  /**
   * 全てのユーザを取得する
   */
  async fetchAll(): Promise<User[] | undefined> {
    const users = await userRepository.fetchAll();

    return users;
  }

  /**
   * レビューを投稿しているユーザを取得する
   */
  async fetchByPostedReview(): Promise<User[] | undefined> {
    const users = await userRepository.fetchByPostedReview();

    return users;
  }
}

export { UserService };
