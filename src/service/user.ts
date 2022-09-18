import { User } from "../model";
import { UserRepository } from "../repository";

const userRepository = new UserRepository();

class UserService {
  /**
   * ユーザを追加・更新する
   */
  async put(user: User): Promise<void> {
    try {
      await userRepository.put(user);
    } catch (error) {
      console.error(error);
    }
  }

  /**
   * ユーザを取得する
   */
  async fetch(userId: string): Promise<User | undefined> {
    try {
      const user = await userRepository.fetch(userId);

      return user;
    } catch (error) {
      console.error(error);
    }
  }

  /**
   * 全てのユーザを取得する
   */
  async fetchAll(): Promise<User[] | undefined> {
    try {
      const users = await userRepository.fetchAll();

      return users;
    } catch (error) {
      console.error(error);
    }
  }

  /**
   * レビューを投稿しているユーザを取得する
   */
  async fetchByPostedReview(): Promise<User[] | undefined> {
    try {
      const users = await userRepository.fetchByPostedReview();

      return users;
    } catch (error) {
      console.error(error);
    }
  }
}

export { UserService };
