import {} from "../model";

class UserActionService {
  /**
   * ユーザの行動履歴を保存する
   */
  async record(params: {
    userId: string;
    actionName: string;
    status: string;
    payload?: any;
  }): Promise<void> {}
}

export { UserActionService };
