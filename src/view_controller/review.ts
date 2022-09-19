import { App } from "@slack/bolt";
import {
  UserService,
  UserActionService,
  BookSearchService,
  ReviewService,
} from "../service";
import { simpleModal, searchBookToReviewModal } from "../view";

const userService = new UserService();
const userActionService = new UserActionService();
const bookSearchService = new BookSearchService();
const reviewService = new ReviewService();

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
  app.action("post_review_action", async ({ ack, client, body }) => {
    await ack();

    if (body.type !== "block_actions") {
      return;
    }

    const userId = body.user.id;

    const user = await userService.fetch(userId);

    if (user) {
      await Promise.all([
        client.views.open({
          trigger_id: body.trigger_id,
          view: searchBookToReviewModal({
            callbackId: "book_search_modal",
          }),
        }),

        userActionService.record({
          userId,
          actionName: "post_review_action",
          status: "ok",
        }),
      ]);
    } else {
      await Promise.all([
        userActionService.record({
          userId,
          actionName: "post_review_action",
          status: "no_user_profile_error",
        }),
        client.views.open({
          trigger_id: body.trigger_id,
          view: simpleModal({
            title: "プロフィールを入力してください",
            text: "レビューを投稿するには、プロフィールの入力が必要です :bow:",
          }),
        }),
      ]);
    }
  });

  /**
   *
   */
  app.view("post_review_modal", async ({ ack, client, logger }) => {
    await ack();

    const isbn = "";

    const book = await bookSearchService.fetchByIsbn(isbn);

    if (!book) {
      throw new Error("Failed to retrieve book.");
    }
  });

  /**
   *
   */
  app.action(
    "open_review_detail_modal_action",
    async ({ client, logger }) => {}
  );
};
