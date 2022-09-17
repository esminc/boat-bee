import { HomeView } from "@slack/bolt";
import { googleGraphic } from "./common";

const totalReviewCount = 10;

/**
 * アプリホーム画面
 */
export const homeView = (props: {
  recommendedBooks: [];
  postReviewActionId: string;
  listUserPostedReviewActionId: string;
  userInfoActionId: string;
  totalReviewCount: number;
  userName: string;
  recommendTimestamp: string;
  booksParams: any;
  privateMetadata: string;
}): HomeView => {
  return {
    type: "home",
    blocks: [
      { type: "divider" },
      {
        type: "header",
        text: { type: "plain_text", text: "本のレビュー", emoji: true },
      },
      {
        type: "section",
        fields: [
          {
            type: "mrkdwn",
            text: `*現在のレビュー投稿数 ${totalReviewCount}件*`,
          },
        ],
      },
      {
        type: "actions",
        elements: [
          {
            type: "button",
            text: {
              type: "plain_text",
              text: "レビューを投稿する :memo:",
              emoji: true,
            },
            value: "dummy_value",
            action_id: props.postReviewActionId,
          },
          {
            type: "button",
            text: {
              type: "plain_text",
              text: "レビューを投稿したユーザ",
              emoji: true,
            },
            value: "dummy_value",
            action_id: props.listUserPostedReviewActionId,
          },
        ],
      },
      {
        type: "header",
        text: { type: "plain_text", text: "ユーザ情報", emoji: true },
      },
      {
        type: "actions",
        elements: [
          {
            type: "button",
            text: {
              type: "plain_text",
              text: "プロフィール",
              emoji: true,
            },
            value: "dummy_value",
            action_id: props.userInfoActionId,
          },
        ],
      },
      { type: "divider" },
      {
        type: "header",
        text: {
          type: "plain_text",
          text: "レビューが投稿されている本",
          emoji: true,
        },
      },
      googleGraphic(),
    ],
  };
};
