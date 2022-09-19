import { ModalView } from "@slack/bolt";
import { User } from "../model";

/**
 * レビューを投稿したユーザモーダル
 */
export const postedReviewUserListModal = (props: {
  callbackId: string;
  users: User[];
}): ModalView => {
  return {
    type: "modal",
    callback_id: props.callbackId,
    title: { type: "plain_text", text: "レビューを投稿したユーザ" },
    close: { type: "plain_text", text: "閉じる", emoji: true },
    blocks: [
      ...(() => {
        if (props.users.length === 0) {
          return [
            {
              type: "section",
              text: {
                type: "plain_text",
                text: "ユーザの取得に失敗しました :expressionless:",
                emoji: true,
              },
            },
          ];
        } else {
          return props.users.map((user) => {
            return {
              type: "section",
              text: {
                type: "mrkdwn",
                text: `*${user.userName}* (${user.postReviewCount})`,
              },
              accessory: {
                type: "button",
                text: {
                  type: "plain_text",
                  text: "このユーザのレビューを見る",
                  emoji: true,
                },
                value: user.userId,
                action_id: "read_review_of_user_action",
              },
            };
          });
        }
      })(),
    ],
  };
};
