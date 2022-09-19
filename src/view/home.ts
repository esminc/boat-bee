import { HomeView, Button } from "@slack/bolt";
import { Book, RecommendBook } from "../model";
import { googleGraphic, bookSection } from "./common";

const totalReviewCount = 10;

/**
 * アプリホーム画面
 */
export const homeView = (props: {
  recommendedBooks?: RecommendBook[];
  postReviewActionId: string;
  listUserPostedReviewActionId: string;
  userInfoActionId: string;
  totalReviewCount: number;
  userName: string;
  recommendTimestamp: string;
  booksParams?: {
    books: Book[];
    showMoveToBack: boolean;
    showMoveToNext: boolean;
  };
  privateMetadata?: string;
}): HomeView => {
  let recommendedBookSections = [];

  if (props.recommendedBooks) {
    props.recommendedBooks.forEach((recommendedBook) => {
      recommendedBookSections.push(bookSection({ ...recommendedBook }));

      recommendedBookSections.push({
        type: "actions",
        elements: [
          {
            type: "button",
            text: {
              type: "plain_text",
              text: recommendedBook.interested ? "興味あり❤️" : "興味なし🤍",
              emoji: true,
            },
            value: `${recommendedBook.isbn}#${recommendedBook.mlModel}`,
            action_id: "button_switch_action",
          },
          {
            type: "button",
            text: {
              type: "plain_text",
              text: "この本のレビューを見る",
              emoji: true,
            },
            value: recommendedBook.isbn,
            action_id: "read_review_of_book_action",
          },
        ],
      });
    });
  } else {
    recommendedBookSections.push({
      type: "section",
      text: {
        type: "plain_text",
        text: "おすすめ本を見るには、レビュー投稿をお願いします :pray:",
        emoji: true,
      },
    });
  }

  return {
    type: "home",
    private_metadata: props.privateMetadata,
    blocks: [
      {
        type: "header",
        text: {
          type: "plain_text",
          text: "読書レビュー共有アプリ「Bee（Book Erabu Eiwa）」 :bee:",
          emoji: true,
        },
      },
      { type: "divider" },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: "*読んだ本のレビューを投稿して、データ蓄積に協力お願いします* ",
        },
      },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: "Beeは、FDOが開発・提供する、本のレビュー共有アプリです。\n仕事で役立った本のレビューを投稿・共有できます。\nデータがたまればたまるほど、AIはより賢くなりあなたに合ったおすすめの本をお伝えすることができます。\n書籍購入制度で購入した本などのレビューを投稿してみましょう！！。",
        },
      },
      { type: "divider" },
      {
        type: "header",
        text: {
          type: "plain_text",
          text: `${props.userName}へのおすすめ本`,
          emoji: true,
        },
      },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: `*最新の推薦データ* : ${props.recommendTimestamp}`,
        },
      },
      ...recommendedBookSections,
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

      ...(() => {
        let bookSections = [];

        if (props.booksParams) {
          props.booksParams.books.forEach((book) => {
            bookSections.push(bookSection({ ...book }));
            bookSections.push({
              type: "actions",
              elements: [
                {
                  type: "button",
                  text: {
                    type: "plain_text",
                    text: "この本のレビューを見る",
                    emoji: true,
                  },
                  value: book.isbn,
                  action_id: "read_review_of_book_action",
                },
              ],
            });
          });

          const moveButtons = { type: "actions", elements: [] as Button[] };

          if (props.booksParams.showMoveToBack) {
            moveButtons.elements.push({
              type: "button",
              text: { type: "plain_text", text: "前へ" },
              action_id: "home_move_to_back_action",
            });
          }

          if (props.booksParams.showMoveToNext) {
            moveButtons.elements.push({
              type: "button",
              text: { type: "plain_text", text: "次へ" },
              action_id: "home_move_to_next_action",
            });
          }

          if (moveButtons.elements.length !== 0) {
            bookSections.push(moveButtons);
          }
        } else {
          bookSections.push({
            type: "section",
            text: {
              type: "plain_text",
              text: "本の取得に失敗しました :expressionless:",
              emoji: true,
            },
          });
        }

        return bookSections;
      })(),
    ],
  };
};
