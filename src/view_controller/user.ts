import { App } from "@slack/bolt";
import { userProfileModal } from "../view";
import { UserService, UserActionService } from "../service";

const userService = new UserService();

export default (app: App) => {
  /**
   *
   */
  app.action("user_info_action", async ({ ack, client, body }) => {
    await ack();

    if (body.type !== "block_actions") {
      return;
    }

    const [user, userInfo] = await Promise.all([
      userService.fetch(body.user.id),
      client.users.info({ user: body.user.id }),
    ]);

    const userName =
      userInfo.user?.profile?.display_name || userInfo.user?.real_name;

    if (!userName) {
      throw new Error("Failed to retrieve user name.");
    }

    await client.views.open({
      view: userProfileModal({
        callbackId: "user_profile_modal",
        userName,
        user,
      }),
      trigger_id: body.trigger_id,
    });
  });
  /**
   *
   */
  app.view("user_profile_modal", async ({ client, logger }) => {});
};
