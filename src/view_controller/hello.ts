import { App } from "@slack/bolt";

export default (app: App) => {
  app.message("hello", async ({ message, say }) => {
    await say(`Hey there!!`);
  });

  app.message("myreview", async ({ message, say }) => {
    await say(`Hey there!!`);
  });
};
