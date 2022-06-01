from logging import getLogger
from typing import Optional

from injector import Injector, inject

from bee_slack_app.model.book import Book
from bee_slack_app.model.review import ReviewContents
from bee_slack_app.repository.book_repository import BookRepository
from bee_slack_app.repository.review_repository import ReviewRepository
from bee_slack_app.repository.user_repository import UserRepository
from bee_slack_app.utils import datetime


class ReviewService:
    @inject
    def __init__(
        self,
        review_repository: ReviewRepository,
        book_repository: BookRepository,
        user_repository: UserRepository,
    ):
        self.review_repository = review_repository
        self.book_repository = book_repository
        self.user_repository = user_repository

    def get_review(self, *, user_id: str, isbn: str) -> Optional[ReviewContents]:
        """
        レビューを一意に指定して取得する
        """
        logger = getLogger(__name__)

        try:
            review = self.review_repository.get(user_id=user_id, isbn=isbn)

            if not review:
                return None

            user = self.user_repository.get(user_id)

            review["user_name"] = user["user_name"] if user else review["user_id"]

            return review

        except Exception:  # pylint: disable=broad-except
            logger.exception("Failed to get data.")
            return None

    def get_review_all(self) -> Optional[list[ReviewContents]]:
        """
        全てのレビューを取得する

        Returns: 取得したレビューのリスト
        """
        logger = getLogger(__name__)

        try:
            reviews = self.review_repository.get_all()

            self.fill_user_name(reviews)

            return reviews

        except Exception:  # pylint: disable=broad-except
            logger.exception("Failed to get data.")
            return None

    def get_reviews_by_isbn(self, *, isbn: str) -> Optional[list[ReviewContents]]:
        """
        ISBNからレビューを取得する
        """
        logger = getLogger(__name__)

        try:
            reviews = self.review_repository.get_by_isbn(isbn=isbn)

            self.fill_user_name(reviews)

            logger.info({"reviews": reviews})

            return reviews

        except Exception:  # pylint: disable=broad-except
            logger.exception("Failed to get data.")
            return None

    def fill_user_name(self, review_contents_list: list[ReviewContents]) -> None:
        # 対応するユーザ情報からユーザ名を取得してレビュー情報に追加する
        users = self.user_repository.get_all()
        for review_contents in review_contents_list:
            user_candidate = [
                user for user in users if user["user_id"] == review_contents["user_id"]
            ]
            if len(user_candidate) == 1:
                user_name = user_candidate[0]["user_name"]
            else:
                # 対応するユーザ情報が存在しない場合はユーザIDを返す
                user_name = review_contents["user_id"]

            review_contents["user_name"] = user_name

    def post_review(self, review_contents: ReviewContents) -> Optional[ReviewContents]:
        logger = getLogger(__name__)

        try:
            updated_at = datetime.now()

            item: ReviewContents = {
                "user_id": review_contents["user_id"],
                "book_title": review_contents["book_title"],
                "isbn": review_contents["isbn"],
                "score_for_me": review_contents["score_for_me"],
                "score_for_others": review_contents["score_for_others"],
                "review_comment": review_contents["review_comment"],
                "updated_at": updated_at,
                "book_image_url": review_contents["book_image_url"],
                "book_author": review_contents["book_author"],
                "book_url": review_contents["book_url"],
                "book_description": review_contents["book_description"],
            }
            self.review_repository.create(item)

            book: Book = {
                "isbn": review_contents["isbn"],
                "title": review_contents["book_title"],
                "author": review_contents["book_author"],
                "url": review_contents["book_url"],
                "image_url": review_contents["book_image_url"],
                "description": review_contents["book_description"],
                "updated_at": updated_at,
            }

            self.book_repository.put(book=book)

            return item

        except Exception as error:  # pylint: disable=broad-except
            logger.exception(f"Failed to store data {error}")
            return None


injector = Injector()

review_service = injector.get(ReviewService)
