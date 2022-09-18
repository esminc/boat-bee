import { ModalView, Block } from "@slack/bolt";
import { googleGraphic, bookSection } from "./common";

/**
 * レビューする本を検索するモーダル
 */
export const searchBookToReviewModal = (props: {
  callbackId: string;
}): ModalView => {
  return {
    type: "modal",
    callback_id: props.callbackId,
    title: { type: "plain_text", text: "レビューする本を検索する" },
    submit: { type: "plain_text", text: "書籍の検索" },
    blocks: [
      {
        type: "input",
        block_id: "input_book_title",
        label: { type: "plain_text", text: "タイトル" },
        element: {
          type: "plain_text_input",
          action_id: "book_title_action",
          placeholder: {
            type: "plain_text",
            text: "本のタイトルを入力してください",
            emoji: true,
          },
        },
      },
      googleGraphic(),
    ],
  };
};

/**
 * レビュー投稿モーダル
 */
export const postReviewModal = (props: {
  callbackId: string;
  bookSectionToReview: Block;
}): ModalView => {
  return {
    type: "modal",
    callback_id: props.callbackId,
    title: { type: "plain_text", text: "Bee" },
    close: { type: "plain_text", text: "戻る", emoji: true },
    submit: { type: "plain_text", text: "送信" },
    blocks: [
      googleGraphic(),
      props.bookSectionToReview,
      {
        type: "input",
        block_id: "input_score_for_me",
        label: { type: "plain_text", text: "自分にとっての評価" },
        element: {
          type: "static_select",
          action_id: "score_for_me_action",
          placeholder: {
            type: "plain_text",
            text: "選択してください",
            emoji: true,
          },
          options: [
            {
              value: "5",
              text: { type: "plain_text", text: "とても良い" },
            },
            {
              value: "4",
              text: { type: "plain_text", text: "良い" },
            },
            {
              value: "3",
              text: { type: "plain_text", text: "普通" },
            },
            {
              value: "2",
              text: { type: "plain_text", text: "悪い" },
            },
            {
              value: "1",
              text: { type: "plain_text", text: "とても悪い" },
            },
          ],
        },
      },
      {
        type: "input",
        block_id: "input_score_for_others",
        label: { type: "plain_text", text: "永和社員へのおすすめ度" },
        element: {
          type: "static_select",
          action_id: "score_for_others_action",
          placeholder: {
            type: "plain_text",
            text: "選択してください",
            emoji: true,
          },
          options: [
            {
              value: "5",
              text: { type: "plain_text", text: "とてもおすすめ" },
            },
            {
              value: "4",
              text: { type: "plain_text", text: "おすすめ" },
            },
            {
              value: "3",
              text: { type: "plain_text", text: "普通" },
            },
            {
              value: "2",
              text: { type: "plain_text", text: "おすすめしない" },
            },
            {
              value: "1",
              text: { type: "plain_text", text: "絶対におすすめしない" },
            },
          ],
        },
      },
      {
        type: "input",
        block_id: "input_comment",
        label: { type: "plain_text", text: "レビューコメント" },
        optional: true,
        element: {
          type: "plain_text_input",
          action_id: "comment_action",
          multiline: true,
        },
      },
      {
        type: "input",
        block_id: "disable_notify_review_post_block",
        optional: true,
        label: {
          type: "plain_text",
          text: "チャンネル #bee へのレビュー投稿通知",
          emoji: true,
        },
        element: {
          type: "checkboxes",
          action_id: "disable_notify_review_post_action",
          options: [
            {
              text: {
                type: "plain_text",
                text: "レビュー投稿を通知しない",
                emoji: true,
              },
              value: "disable_notify_review_post",
            },
          ],
        },
      },
    ],
  };
};
