import { App } from "@slack/bolt";
import { homeView } from "../view";
import {
  ReviewService,
  UserService,
  UserActionService,
  BookService,
  RecommendService,
} from "../service";

const BOOK_NUMBER_PER_PAGE = 20;

const bookService = new BookService();
const reviewService = new ReviewService();
const recommendService = new RecommendService();
const userService = new UserService();
const userActionService = new UserActionService();

export default (app: App) => {
  /**
   * ホーム画面
   */
  app.event("app_home_opened", async ({ event, client, logger }) => {
    const reviews = await reviewService.fetchAll();

    const totalReviewCount = reviews?.length || 0;

    const recommendTimestamp = "";

    await userActionService.record({
      userId: event.user,
      actionName: "app_home_opened",
      status: "ok",
      payload: { total_review_count: totalReviewCount },
    });

    const user = await userService.fetch(event.user);
    const userName = user ? `${user.userName}さん` : "あなた";

    const recommendedBooks = await recommendService.fetch(event.user);

    const books = await bookService.fetch({ limit: BOOK_NUMBER_PER_PAGE });

    let booksParams = undefined;
    let privateMetadata = undefined;

    if (books) {
      booksParams = {
        books: books.items,
        showMoveToBack: false,
        showMoveToNext: books.hasNext,
      };

      privateMetadata = privateMetadataConverter.toPrivateMetadata(books.keys);
    }

    await client.views.publish({
      user_id: event.user,
      view: homeView({
        recommendedBooks,
        postReviewActionId: "post_review_action",
        listUserPostedReviewActionId: "list_user_posted_review_action",
        userInfoActionId: "user_info_action",
        totalReviewCount,
        userName,
        recommendTimestamp,
        booksParams,
        privateMetadata,
      }),
    });
  });

  /**
   * ホーム画面で「次へ」を押下されたときの処理
   */
  app.action("home_move_to_next_action", async ({ ack, client, body }) => {
    await ack();

    if (body.type !== "block_actions" || !body.view) {
      return;
    }

    const userId = body.user.id;
    const privateMetadataBefore = privateMetadataConverter.toObject(
      body.view.private_metadata
    );

    const reviews = await reviewService.fetchAll();

    const totalReviewCount = reviews?.length || 0;

    const recommendTimestamp = "";

    const user = await userService.fetch(userId);
    const userName = user ? `${user.userName}さん` : "あなた";

    const recommendedBooks = await recommendService.fetch(userId);

    const books = await bookService.fetch({
      limit: BOOK_NUMBER_PER_PAGE,
      keys: privateMetadataBefore.keys,
    });

    console.info({ books });

    let booksParams = undefined;
    let privateMetadata = undefined;

    if (books) {
      booksParams = {
        books: books.items,
        showMoveToBack: true,
        showMoveToNext: books.hasNext,
      };

      privateMetadata = privateMetadataConverter.toPrivateMetadata(books.keys);
    }

    await client.views.publish({
      user_id: userId,
      view: homeView({
        recommendedBooks,
        postReviewActionId: "post_review_action",
        listUserPostedReviewActionId: "list_user_posted_review_action",
        userInfoActionId: "user_info_action",
        totalReviewCount,
        userName,
        recommendTimestamp,
        booksParams,
        privateMetadata,
      }),
    });
  });

  /**
   * ホーム画面で「前へ」を押下されたときの処理
   */
  app.action("home_move_to_back_action", async ({ ack, client, body }) => {
    await ack();

    if (body.type !== "block_actions" || !body.view) {
      return;
    }

    const userId = body.user.id;
    const privateMetadataBefore = privateMetadataConverter.toObject(
      body.view.private_metadata
    );

    const reviews = await reviewService.fetchAll();

    const totalReviewCount = reviews?.length || 0;

    const recommendTimestamp = "";

    const user = await userService.fetch(userId);
    const userName = user ? `${user.userName}さん` : "あなた";

    const recommendedBooks = await recommendService.fetch(userId);

    const books = await bookService.fetchBefore({
      limit: BOOK_NUMBER_PER_PAGE,
      keys: privateMetadataBefore.keys,
    });

    console.info({ books });

    let booksParams = undefined;
    let privateMetadata = undefined;

    if (books) {
      booksParams = {
        books: books.items,
        showMoveToBack: !books.isMoveToFirst,
        showMoveToNext: true,
      };

      privateMetadata = privateMetadataConverter.toPrivateMetadata(books.keys);
    }

    await client.views.publish({
      user_id: userId,
      view: homeView({
        recommendedBooks,
        postReviewActionId: "post_review_action",
        listUserPostedReviewActionId: "list_user_posted_review_action",
        userInfoActionId: "user_info_action",
        totalReviewCount,
        userName,
        recommendTimestamp,
        booksParams,
        privateMetadata,
      }),
    });
  });
};

const privateMetadataConverter = {
  toPrivateMetadata: function (keys: any[]) {
    return JSON.stringify({ keys: keys });
  },
  toObject: function (privateMetadata: string): { keys: any[] } {
    return JSON.parse(privateMetadata);
  },
};
