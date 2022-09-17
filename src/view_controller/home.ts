import { App } from "@slack/bolt";
import { Home } from "../view";
import { ReviewService } from "../service";

const BOOK_NUMBER_PER_PAGE = 20;

const reviewService = new ReviewService();

export default (app: App) => {
  /**
   * ホーム画面
   */
  app.event("app_home_opened", async ({ event, client, logger }) => {
    await client.views.publish({
      user_id: event.user,
      view: Home.homeView,
    });
  });

  /**
   * ホーム画面で「次へ」を押下されたときの処理
   */
  app.action("home_move_to_next_action", async ({ client, logger }) => {
    await client.views.update({
      view: Home.homeView,
    });
  });

  /**
   * ホーム画面で「前へ」を押下されたときの処理
   */
  app.action("home_move_to_back_action", async ({ client, logger }) => {
    await client.views.update({
      view: Home.homeView,
    });
  });
};
