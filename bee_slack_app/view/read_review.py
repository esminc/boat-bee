from typing import TypedDict

from bee_slack_app.model.review import ReviewContents
from bee_slack_app.utils import datetime
from bee_slack_app.view.common import book_section


class BookOfReview(TypedDict):
    isbn: str
    title: str
    author: str
    url: str
    image_url: str


def review_modal(
    *, callback_id: str, book: BookOfReview, reviews: list[ReviewContents]
):
    """
    レビューモーダル

    Args:
        callback_id: モーダルのcallback_id
        book: レビュー対象の本
        reviews: 表示するレビューのリスト
    """

    view = {
        "type": "modal",
        "callback_id": callback_id,
        "title": {"type": "plain_text", "text": "本のレビュー"},
        "blocks": [
            {
                "type": "image",
                "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
                "alt_text": "Google Logo",
            },
            book_section(
                title=book["title"],
                author=book["author"],
                isbn=book["isbn"],
                url=book["url"],
                image_url=book["image_url"],
            ),
            {"type": "divider"},
        ],
    }

    review_blocks = []

    for review in reviews:

        update_datetime = (
            datetime.parse(review["updated_at"]) if review["updated_at"] else "-"
        )

        review_blocks.append(
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*投稿者*\n{review['user_name']}",
                    },  # type:ignore
                    {
                        "type": "mrkdwn",
                        "text": f"*投稿日時*\n{update_datetime}",
                    },  # type:ignore
                    {  # type:ignore
                        "type": "mrkdwn",
                        "text": f"*自分にとっての評価*\n{review['score_for_me']}",
                    },
                    {  # type:ignore
                        "type": "mrkdwn",
                        "text": f"*永和社員へのおすすめ度*\n{review['score_for_others']}",
                    },
                ],
            }
        )

        review_blocks.append(
            {
                "type": "section",
                "text": {  # type:ignore
                    "type": "mrkdwn",
                    "text": f"*レビューコメント*\n\n{review['review_comment'] or '-'}",
                },
            }
        )

        review_blocks.append(
            {  # pylint: disable=duplicate-code
                "type": "actions",
                "elements": [
                    {  # type: ignore
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "もっと見る",
                            "emoji": True,
                        },
                        "value": review["user_id"] + ":" + review["isbn"],
                        "action_id": "open_review_detail_modal_action",
                    }
                ],
            },
        )

        review_blocks.append({"type": "divider"})

    view["blocks"].extend(review_blocks)  # type: ignore

    return view


def review_of_user_modal(*, callback_id: str, reviews: list[ReviewContents]):
    """
    ユーザのレビューモーダル

    Args:
        callback_id: モーダルのcallback_id
        reviews: 表示するレビューのリスト
    """

    view = {
        "type": "modal",
        "callback_id": callback_id,
        "title": {"type": "plain_text", "text": "本のレビュー"},
        "blocks": [
            {
                "type": "image",
                "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
                "alt_text": "Google Logo",
            },
            {"type": "divider"},
        ],
    }

    review_blocks = []

    for review in reviews:

        update_datetime = (
            datetime.parse(review["updated_at"]) if review["updated_at"] else "-"
        )

        review_blocks.append(
            book_section(
                title=review["book_title"],
                author=review["book_author"],
                isbn=review["isbn"],
                url=review["book_url"],
                image_url=review["book_image_url"],
            )
        )

        review_blocks.append(
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*投稿者*\n{review['user_name']}",
                    },  # type:ignore
                    {
                        "type": "mrkdwn",
                        "text": f"*投稿日時*\n{update_datetime}",
                    },  # type:ignore
                    {  # type:ignore
                        "type": "mrkdwn",
                        "text": f"*自分にとっての評価*\n{review['score_for_me']}",
                    },
                    {  # type:ignore
                        "type": "mrkdwn",
                        "text": f"*永和社員へのおすすめ度*\n{review['score_for_others']}",
                    },
                ],
            }
        )

        review_blocks.append(
            {
                "type": "section",
                "text": {  # type:ignore
                    "type": "mrkdwn",
                    "text": f"*レビューコメント*\n\n{review['review_comment'] or '-'}",
                },
            }
        )

        review_blocks.append(
            {  # pylint: disable=duplicate-code
                "type": "actions",
                "elements": [
                    {  # type: ignore
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "もっと見る",
                            "emoji": True,
                        },
                        "value": review["user_id"] + ":" + review["isbn"],
                        "action_id": "open_review_detail_modal_action",
                    }
                ],
            },
        )

        review_blocks.append({"type": "divider"})

    view["blocks"].extend(review_blocks)  # type: ignore

    return view


def review_detail_modal(review_contents: ReviewContents):
    """
    レビュー詳細モーダル

    Args:
        review_contents: 表示するレビュー
    """

    update_datetime = (
        datetime.parse(review_contents["updated_at"])
        if review_contents["updated_at"]
        else "-"
    )

    review_comment = review_contents["review_comment"] or "-"

    return {
        "type": "modal",
        "title": {"type": "plain_text", "text": "レビュー詳細", "emoji": True},
        "close": {"type": "plain_text", "text": "戻る", "emoji": True},
        "blocks": [
            book_section(
                title=review_contents["book_title"],
                author=review_contents["book_author"],
                isbn=review_contents["isbn"],
                url=review_contents["book_url"],
                image_url=review_contents["book_image_url"],
            ),
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*投稿者*\n{review_contents['user_name']}",
                    },  # type:ignore
                    {
                        "type": "mrkdwn",
                        "text": f"*投稿日時*\n{update_datetime}",
                    },  # type:ignore
                    {  # type:ignore
                        "type": "mrkdwn",
                        "text": f"*自分にとっての評価*\n{review_contents['score_for_me']}",
                    },
                    {  # type:ignore
                        "type": "mrkdwn",
                        "text": f"*永和社員へのおすすめ度*\n{review_contents['score_for_others']}",
                    },
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*レビューコメント*\n\n{review_comment}",
                },
            },
        ],
    }
