/**
 * テキストだけの簡易モーダル
 */
export const simpleModal = (props: { title: string; text: string }) => {
  return {
    type: "modal",
    title: { type: "plain_text", text: props.title, emoji: true },
    close: { type: "plain_text", text: "OK", emoji: true },
    blocks: [
      {
        type: "section",
        text: {
          type: "plain_text",
          text: props.text,
          emoji: true,
        },
      },
    ],
  };
};

const DUMMY_IMAGE_URL =
  "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg";

/**
 * 本のセクション
 */
export const bookSection = (props: {
  title: string;
  author: string;
  isbn: string;
  url: string;
  imageUrl?: string;
}) => {
  return {
    type: "section",
    text: {
      type: "mrkdwn",
      text: `*${props.title}*\n${props.author}\nISBN-${props.isbn}\n<${props.url}|Google Booksで見る>`,
    },
    accessory: {
      type: "image",
      image_url: props.imageUrl || DUMMY_IMAGE_URL,
      alt_text: props.title,
    },
  };
};

/**
 * 「Powered by Google」
 */
export const googleGraphic = () => {
  return {
    type: "section",
    text: {
      type: "mrkdwn",
      text: "Powered by Google",
    },
  };
};
