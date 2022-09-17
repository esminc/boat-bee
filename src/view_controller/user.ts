import { App } from "@slack/bolt";

export default (app: App) => {
  /**
   *
   */
  app.action("user_info_action", async ({ client, logger }) => {});
  /**
   *
   */
  app.view("user_profile_modal", async ({ client, logger }) => {});
};
