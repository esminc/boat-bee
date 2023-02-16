from typing import Any, TypedDict

from bee_slack_app.model import Review, ReviewPagination
from bee_slack_app.utils import datetime
from bee_slack_app.view.common import book_section, google_graphic


class BookOfReview(TypedDict):
    isbn: str
    title: str
    author: str
    url: str
    image_url: str


def review_modal(*, callback_id: str, book: BookOfReview, reviews: list[Review]):
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
            google_graphic(),
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

        review_blocks.extend(
            _review_sections(
                user_name=review["user_name"],
                update_datetime=update_datetime,
                score_for_me=review["score_for_me"],
                score_for_others=review["score_for_others"],
                review_comment=review["review_comment"],
            )
        )

        review_blocks.append(
            _review_detail_button(user_id=review["user_id"], isbn=review["isbn"])
        )

        review_blocks.append({"type": "divider"})

    view["blocks"].extend(review_blocks)  # type: ignore

    return view


def review_of_user_modal(
    *, callback_id: str, reviews_param: ReviewPagination, private_metadata: str
):
    """
    ユーザのレビューモーダル

    Args:
        callback_id: モーダルのcallback_id
        reviews_param: 「投稿されているレビュー」のデータ
        private_metadata: private_metadata

    """

    view = {
        "type": "modal",
        "private_metadata": private_metadata,
        "callback_id": callback_id,
        "title": {"type": "plain_text", "text": "本のレビュー"},
        "blocks": [
            google_graphic(),
            {"type": "divider"},
        ],
    }

    review_blocks = []

    move_buttons = {"type": "actions", "elements": []}

    for review in reviews_param["reviews"]:

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

        review_blocks.extend(
            _review_sections(
                user_name=review["user_name"],
                update_datetime=update_datetime,
                score_for_me=review["score_for_me"],
                score_for_others=review["score_for_others"],
                review_comment=review["review_comment"],
            )
        )

        review_blocks.append(
            _review_detail_button(user_id=review["user_id"], isbn=review["isbn"])
        )

        review_blocks.append({"type": "divider"})

    if reviews_param["show_move_to_back"]:
        move_buttons["elements"] = [
            {  # type: ignore
                "type": "button",
                "text": {"type": "plain_text", "text": "前へ"},
                "action_id": "review_move_to_back_action",
            }
        ]

    if reviews_param["show_move_to_next"]:
        move_buttons["elements"] = move_buttons["elements"] + [  # type: ignore
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "次へ"},
                "action_id": "review_move_to_next_action",
            }
        ]

    if bool(move_buttons["elements"]):
        review_blocks.append(move_buttons)

    view["blocks"].extend(review_blocks)  # type: ignore

    return view


def review_detail_modal(review_contents: Review) -> dict[str, Any]:
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
            *_review_sections(
                user_name=review_contents["user_name"],
                update_datetime=update_datetime,
                score_for_me=review_contents["score_for_me"],
                score_for_others=review_contents["score_for_others"],
                review_comment=review_contents["review_comment"],
            ),
        ],
    }


def _review_sections(
    *,
    user_name: str,
    update_datetime: str,
    score_for_me: str,
    score_for_others: str,
    review_comment: str,
):
    """
    レビューのセクションのリスト
    """
    return [
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*投稿者*\n{user_name}",
                },
                {
                    "type": "mrkdwn",
                    "text": f"*投稿日時*\n{update_datetime}",
                },
                {
                    "type": "mrkdwn",
                    "text": f"*自分にとっての評価*\n{score_for_me}",
                },
                {
                    "type": "mrkdwn",
                    "text": f"*永和社員へのおすすめ度*\n{score_for_others}",
                },
            ],
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*レビューコメント*\n\n{review_comment or '-'}",
            },
        },
    ]


def _review_detail_button(*, user_id: str, isbn: str):
    """
    レビューの「もっと見る」ボタン

    actionのvalueは '<user_id>:<isbn>'
    """
    return {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "もっと見る",
                    "emoji": True,
                },
                "value": user_id + ":" + isbn,
                "action_id": "open_review_detail_modal_action",
            }
        ],
    }
