import { Review } from "../model";
import { now } from "../utils/datetime";
import {
  ReviewRepository,
  UserRepository,
  BookRepository,
} from "../repository";

const reviewRepository = new ReviewRepository();
const userRepository = new UserRepository();
const bookRepository = new BookRepository();

class ReviewService {
  /**
   * レビューを取得する
   */
  async fetch(userId: string, isbn: string): Promise<Review | null> {
    const [review, user] = await Promise.all([
      reviewRepository.fetch(userId, isbn),
      userRepository.fetch(userId),
    ]);

    if (!review) {
      return null;
    }

    const userName = user ? user.userName : review.userId;

    return { ...review, userName };
  }

  /**
   * 全てのレビューを取得する
   */
  async fetchAll(): Promise<Review[] | null> {
    const reviews = await reviewRepository.fetchAll();

    if (!reviews) {
      return null;
    }

    return this.fillUserName(reviews);
  }

  /**
   * ユーザIDからレビューを取得する
   */
  async fetchByUserId(userId: string): Promise<Review[] | null> {
    const reviews = await reviewRepository.fetchByUserId(userId);

    if (!reviews) {
      return null;
    }

    return this.fillUserName(reviews);
  }
  /**
   * ユーザIDからレビューを順方向に取得する
   */
  async fetchNextByUserId(userId: string): Promise<Review[] | undefined> {
    return undefined;
  }

  /**
   * ユーザIDからレビューを逆方向に取得する
   */
  async fetchBackByUserId(userId: string): Promise<Review[] | undefined> {
    return undefined;
  }

  /**
   * レビューを追加・更新する
   */
  async put(review: Review): Promise<void> {
    const updatedAt = now();

    const book = {
      isbn: review.isbn,
      title: review.bookTitle,
      author: review.bookAuthor,
      url: review.bookUrl,
      imageUrl: review.bookImageUrl,
      description: review.bookDescription,
      updatedAt,
    };

    await Promise.all([
      (bookRepository.put(book), reviewRepository.put(review)),
    ]);

    const postReviewCount = (
      await reviewRepository.fetchByUserId(review.userId)
    )?.length;

    if (!postReviewCount) {
      return;
    }

    await userRepository.updatePostReviewCount(review.userId, postReviewCount);
  }

  /**
   * ユーザ名をレビューに追加する
   */
  // TODO: 戻り値ではuser_nameがnon-nullなので、型を絞る
  private async fillUserName(target: Review[]): Promise<Review[]> {
    const users = await userRepository.fetchAll();

    if (!users) {
      // ユーザ情報が存在しない場合は、ユーザIDをユーザ名に設定する
      return target.map((review) => {
        return { ...review, userName: review.userId };
      });
    }

    return target.map((review) => {
      const user = users.find((user) => user.userId === review.userId);

      let userName = undefined;

      if (user) {
        userName = user.userName;
      } else {
        // ユーザ情報が存在しない場合は、ユーザIDをユーザ名に設定する
        userName = review.userId;
      }

      return { ...review, userName };
    });
  }
}

export { ReviewService };
