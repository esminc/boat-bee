from typing import TypedDict

from .contents_based_filtering import BeeContentsBaseRecommender
from .filter import filter_books_no_post_review, filter_books_no_suggested
from .random_recommend import BeeRandomRecommender
from .types import Review, SuggestedBook

BookRecommendation = TypedDict(
    "BookRecommendation", {"ml_model_name": str, "isbn": str}
)

UserId = str

TrainAndPredictResult = dict[UserId, list[BookRecommendation]]


def train_and_predict(
    reviews: list[Review], suggested_books: list[SuggestedBook]
) -> TrainAndPredictResult:
    ml_models = [
        {
            "ml_model_name": "contents_based_filtering",
            "recommender": BeeContentsBaseRecommender(reviews, suggested_books),
        },
        {
            "ml_model_name": "random_recommendation",
            "recommender": BeeRandomRecommender(reviews),
        },
        {
            "ml_model_name": "random_recommendation",
            "recommender": BeeRandomRecommender(reviews),
        },
    ]

    user_id_set = {review["user_id"] for review in reviews}
    books_set = {review["isbn"] for review in reviews}

    result = {user_id: [] for user_id in user_id_set}

    for ml_model in ml_models:

        ml_model_recommender = ml_model["recommender"]

        ml_model_recommender.train()

        for user_id in user_id_set:

            books = ml_model_recommender.predict(user_id, len(books_set))

            books_without_review = filter_books_no_post_review(user_id, books, reviews)

            books_without_review_and_no_suggested = filter_books_no_suggested(
                user_id, books_without_review, suggested_books
            )

            recommended_book = (
                books_without_review_and_no_suggested[0]
                if books_without_review_and_no_suggested
                else books[0]
            )

            result[user_id].append(
                {"ml_model_name": ml_model["ml_model_name"], "isbn": recommended_book}
            )

    return result
