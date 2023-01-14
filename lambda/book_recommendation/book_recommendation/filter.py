from book_recommendation.types import Review, SuggestedBook


def filter_books_no_post_review(
    user_id: str, books: list[str], reviews: list[Review]
) -> list[str]:
    """
    このユーザがレビューを投稿していない本だけを取り出す

    Args:
        user_id: フィルタしたい対象のユーザID
        books: フィルタしたい本のISBNのリスト
        reviews: 投稿されたレビューのリスト
    Returns:
        レビューを投稿していない本のISBNのリスト
    """
    review_books_isbn_of_user = {
        review["isbn"] for review in reviews if review["user_id"] == user_id
    }

    return [book for book in books if book not in review_books_isbn_of_user]


def filter_books_no_suggested(
    user_id: str, books: list[str], suggested_books: list[SuggestedBook]
) -> list[str]:
    """
    このユーザがおすすめされていない本だけを取り出す

    Args:
        user_id: フィルタしたい対象のユーザID
        books: フィルタしたい本のISBNのリスト
        suggested_books: おすすめされた本のリスト
    Returns:
        おすすめされていない本のISBNのリスト
    """
    suggested_books_isbn_of_user = {
        suggested_book["isbn"]
        for suggested_book in suggested_books
        if suggested_book["user_id"] == user_id
    }

    return [book for book in books if book not in suggested_books_isbn_of_user]
