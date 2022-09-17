import { App } from "@slack/bolt";

export default (app: App) => {
  app.message("hello", async ({ message, say }) => {
    await say(`Hey there!!`);
  });

  app.command("/bee", async ({ say }) => {
    await say({ text: "Hey there", reply_broadcast: false });
  });
};
