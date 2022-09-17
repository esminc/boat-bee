import { Review } from "../model";
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
    try {
      const [review, user] = await Promise.all([
        reviewRepository.fetch(userId, isbn),
        userRepository.fetch(userId),
      ]);

      if (!review) {
        return null;
      }

      const userName = user ? user.user_name : review.user_id;

      return { ...review, user_name: userName };
    } catch (error) {
      console.error(error);

      return null;
    }
  }

  /**
   * 全てのレビューを取得する
   */
  async fetchAll(): Promise<Review[] | null> {
    try {
      const reviews = await reviewRepository.fetchAll();

      if (!reviews) {
        return null;
      }

      return this.fillUserName(reviews);
    } catch (error) {
      console.error(error);

      return null;
    }
  }

  /**
   * ユーザIDからレビューを取得する
   */
  async fetchByUserId(userId: string): Promise<Review[] | null> {
    try {
      const reviews = await reviewRepository.fetchByUserId(userId);

      if (!reviews) {
        return null;
      }

      return this.fillUserName(reviews);
    } catch (error) {
      console.error(error);

      return null;
    }
  }
  /**
   * ユーザIDからレビューを順方向に取得する
   */
  async fetchNextByUserId(userId: string): Promise<Review[] | null> {
  }

  /**
   * ユーザIDからレビューを逆方向に取得する
   */
   async fetchBackByUserId(userId: string): Promise<Review[] | null> {
  }


  /**
   * レビューを追加・更新する
   */
  async put(params: {}): Promise<void> {
    try {
      const review = {};
      const book = {};

      await Promise.all([
        (bookRepository.put(book), reviewRepository.put(review)),
      ]);

      const postReviewCount = (await reviewRepository.fetchByUserId())?.length;

      if (!postReviewCount) {
        return;
      }

      await userRepository.updatePostReviewCount(, postReviewCount)

    } catch (error) {
      console.error(error);

    }
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
        return { ...review, user_name: review.user_id };
      });
    }

    return target.map((review) => {
      const user = users.find((user) => user.user_id === review.user_id);

      let userName = undefined;

      if (user) {
        userName = user.user_name;
      } else {
        // ユーザ情報が存在しない場合は、ユーザIDをユーザ名に設定する
        userName = review.user_id;
      }

      return { ...review, user_name: userName };
    });
  }
}

export { ReviewService };
