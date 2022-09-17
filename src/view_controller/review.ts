import { App } from "@slack/bolt";

export default (app: App) => {
  /**
   * 本のレビューモーダルを開く
   */
  app.action("read_review_of_book_action", async ({ client, logger }) => {});
  /**
   * 選択したユーザのレビューリストを開く
   */
  app.action("read_review_of_user_action", async ({ client, logger }) => {});
  /**
   * レビューリストで「次へ」を押下されたときの処理
   */
  app.action("review_move_to_next_action", async ({ client, logger }) => {});
  /**
   * レビューリストで「前へ」を押下されたときの処理
   */
  app.action("review_move_to_back_action", async ({ client, logger }) => {});
  /**
   * 本の検索モーダルを開く
   */
  app.action("post_review_action", async ({ client, logger }) => {});
  /**
   *
   */
  app.view("post_review_modal", async ({ client, logger }) => {});
  /**
   *
   */
  app.action(
    "open_review_detail_modal_action",
    async ({ client, logger }) => {}
  );
};
