/**
 * ユーザの行動履歴
 */
export type UserAction = {
  userId: string;
  createdAt: string;
  actionName: string;
  status: string;
  payload?: any;
};
