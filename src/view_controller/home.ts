import { App } from "@slack/bolt";
import { homeView } from "../view";
import { ReviewService, UserService } from "../service";

const BOOK_NUMBER_PER_PAGE = 20;

const reviewService = new ReviewService();
const userService = new UserService();

export default (app: App) => {
  /**
   * ホーム画面
   */
  app.event("app_home_opened", async ({ event, client, logger }) => {
    const reviews = await reviewService.fetchAll();

    const totalReviewCount = reviews?.length || 0;

    const recommendTimestamp = "";

    const user = await userService.fetch(event.user);
    const userName = user ? `${user.user_name}さん` : "あなた";

    const recommendedBooks = [];

    await client.views.publish({
      user_id: event.user,
      view: homeView({
        recommendedBooks,
        postReviewActionId,
        listUserPostedReviewActionId,
        userInfoActionId,
        totalReviewCount,
        userName,
        recommendTimestamp,
        booksParams,
        privateMetadata,
      }),
    });
  });

  /**
   * ホーム画面で「次へ」を押下されたときの処理
   */
  app.action("home_move_to_next_action", async ({ client, logger }) => {
    await client.views.update({
      view: homeView(),
    });
  });

  /**
   * ホーム画面で「前へ」を押下されたときの処理
   */
  app.action("home_move_to_back_action", async ({ client, logger }) => {
    await client.views.update({
      view: homeView(),
    });
  });
};
