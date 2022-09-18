import { ModalView, KnownBlock } from "@slack/bolt";
import { SearchedBook } from "../model";
import { googleGraphic } from "./common";

/**
 * 本の検索結果モーダル
 */
export const bookSearchResultModal = (props: {
  callbackId: string;
  privateMetadata: string;
  searchedBooks: SearchedBook[];
}): ModalView => {
  return {
    type: "modal",
    callback_id: props.callbackId,
    private_metadata: props.privateMetadata,
    title: { type: "plain_text", text: "書籍の検索結果", emoji: true },
    close: { type: "plain_text", text: "戻る", emoji: true },
    submit: { type: "plain_text", text: "決定", emoji: true },
    blocks: [
      googleGraphic(),
      ...(() => {
        const DUMMY_IMAGE_URL =
          "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg";

        const blocks: KnownBlock[] = [];

        props.searchedBooks.map((searchedBook) => {
          const imageUrl = searchedBook.imageUrl || DUMMY_IMAGE_URL;

          const authors = searchedBook.authors.join(", ");

          blocks.push({ type: "divider" });
          blocks.push({
            type: "section",
            text: {
              type: "mrkdwn",
              text: `*${searchedBook.title}*\n${authors}\nISBN-${searchedBook.isbn}`,
            },
            accessory: {
              type: "image",
              image_url: imageUrl,
              alt_text: "Windsor Court Hotel thumbnail",
            },
          });
          blocks.push({
            type: "actions",
            elements: [
              {
                type: "button",
                text: { type: "plain_text", text: "選択", emoji: true },
                value: searchedBook.isbn,
                action_id: "select_book_action",
              },
              {
                type: "button",
                text: {
                  type: "plain_text",
                  text: "Google Booksで見る",
                  emoji: true,
                },
                url: searchedBook.googleBooksUrl,
                action_id: "google_books_buttons_action",
              },
            ],
          });
        });

        return blocks;
      })(),
    ],
  };
};
