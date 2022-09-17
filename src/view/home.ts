import { HomeView } from "@slack/bolt";

export const homeView: HomeView = {
  type: "home",
  blocks: [
    {
      type: "section",
      text: {
        type: "mrkdwn",
        text: "Welcome home",
      },
    },
    {
      type: "section",
      text: {
        type: "mrkdwn",
        text: "Learn how home tabs can be more useful and interactive <https://api.slack.com/surfaces/tabs/using|*in the documentation*>.",
      },
    },
  ],
};
