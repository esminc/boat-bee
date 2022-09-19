import { App } from "@slack/bolt";
import { postedReviewUserListModal } from "../view";
import { UserService } from "../service";

const userService = new UserService();

export default (app: App) => {
  /**
   * 「レビューを投稿したユーザ」ボタンが押下されたとき
   */
  app.action(
    "list_user_posted_review_action",
    async ({ ack, client, body }) => {
      await ack();

      if (body.type !== "block_actions") {
        return;
      }

      const users = await userService.fetchByPostedReview();

      if (!users) {
        throw new Error("Failed to retrieve users.");
      }

      await client.views.open({
        trigger_id: body.trigger_id,
        view: postedReviewUserListModal({
          callbackId: "review_modal",
          users,
        }),
      });
    }
  );
};
