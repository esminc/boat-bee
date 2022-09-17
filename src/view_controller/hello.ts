import { App } from "@slack/bolt";

export default (app: App) => {
  app.message("hello", async ({ message, say }) => {
    await say(`Hey there!!`);
  });

  app.command("/bee", async ({ ack, respond }) => {
    await ack();

    await respond({ response_type: "ephemeral", text: "Hey there" });
  });
};
