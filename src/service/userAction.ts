import { now } from "../utils/datetime";
import { UserActionRepository } from "../repository";

const userActionRepository = new UserActionRepository();

class UserActionService {
  /**
   * ユーザの行動履歴を保存する
   */
  async record(params: {
    userId: string;
    actionName: string;
    status: string;
    payload?: any;
  }): Promise<void> {
    const item = { ...params, createdAt: now() };

    console.info(item);

    await userActionRepository.put(item);
  }
}

export { UserActionService };
