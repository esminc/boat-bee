import { ModalView, Block, SectionBlock } from "@slack/bolt";
import { Book, Review } from "../model";
import { googleGraphic, bookSection } from "./common";

/**
 * レビューモーダル
 */
export const reviewModal = (props: {
  callbackId: string;
  book: Book;
  reviews: Review[];
}): ModalView => {
  return {
    type: "modal",
    callback_id: props.callbackId,
    title: { type: "plain_text", text: "本のレビュー" },
    blocks: [
      googleGraphic(),
      bookSection({ ...props.book }),
      { type: "divider" },
      ...(() => {
        let reviewBlocks: Block[] = [];

        props.reviews.forEach((review) => {
          reviewBlocks.push(
            bookSection({
              title: review.bookTitle,
              author: review.bookAuthor,
              isbn: review.isbn,
              url: review.isbn,
              imageUrl: review.bookImageUrl,
            })
          );

          reviewBlocks = [...reviewBlocks, ...reviewSectionList({ review })];

          reviewBlocks.push(
            reviewDetailButton({ userId: review.userId, isbn: review.isbn })
          );

          reviewBlocks.push({ type: "divider" });
        });

        return reviewBlocks;
      })(),
    ],
  };
};

/**
 * レビュー詳細モーダル
 */
export const reviewDetailModal = (props: { review: Review }): ModalView => {
  return {
    type: "modal",
    title: { type: "plain_text", text: "レビュー詳細", emoji: true },
    close: { type: "plain_text", text: "戻る", emoji: true },
    blocks: [
      bookSection({
        title: props.review.bookTitle,
        author: props.review.bookAuthor,
        isbn: props.review.isbn,
        url: props.review.isbn,
        imageUrl: props.review.bookImageUrl,
      }),
      ...reviewSectionList({ review: props.review }),
    ],
  };
};

/**
 * レビューセクションのリスト
 */
const reviewSectionList = (props: { review: Review }) => {
  return [
    {
      type: "section",
      fields: [
        {
          type: "mrkdwn",
          text: `*投稿者*\n${props.review.userId}`,
        },
        {
          type: "mrkdwn",
          text: `*投稿日時*\n${props.review.updatedAt}`,
        },
        {
          type: "mrkdwn",
          text: `*自分にとっての評価*\n${props.review.scoreForMe}`,
        },
        {
          type: "mrkdwn",
          text: `*永和社員へのおすすめ度*\n${props.review.scoreForOthers}`,
        },
      ],
    },
    {
      type: "section",
      text: {
        type: "mrkdwn",
        text: `*レビューコメント*\n\n${props.review.reviewComment || "-"}`,
      },
    },
  ];
};

/**
 * レビューの「もっと見る」ボタン
 *
 * actionのvalueは '<userId>:<isbn>'
 */
const reviewDetailButton = (props: { userId: string; isbn: string }) => {
  return {
    type: "actions",
    elements: [
      {
        type: "button",
        text: {
          type: "plain_text",
          text: "もっと見る",
          emoji: true,
        },
        value: props.userId + ":" + props.isbn,
        action_id: "open_review_detail_modal_action",
      },
    ],
  };
};
