from typing import Any

from bee_slack_app.model import SearchedBook
from bee_slack_app.view.common import DUMMY_IMAGE_URL, google_graphic


def book_search_result_modal(
    *,
    callback_id: str,
    private_metadata: str,
    book_results: list[SearchedBook],
):
    """
    本の検索結果モーダル

    Args:
        callback_id: モーダルのcallback_id
        private_metadata: モーダルのprivate_metadata
        book_results: 本の検索結果のリスト
    """
    blocks = []
    blocks.append(google_graphic())

    for book in book_results:
        blocks.extend(_generate_book_block(book))

    view = {
        "type": "modal",
        "callback_id": callback_id,
        "private_metadata": private_metadata,
        "title": {
            "type": "plain_text",
            "text": "書籍の検索結果",
            "emoji": True,
        },
        "close": {"type": "plain_text", "text": "戻る", "emoji": True},
        "submit": {"type": "plain_text", "text": "決定", "emoji": True},
        "blocks": blocks,
    }

    return view


def _generate_book_block(book: SearchedBook):
    authors = ", ".join(book["authors"])
    image_url = book["image_url"] if book["image_url"] is not None else DUMMY_IMAGE_URL

    block = [
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{book['title']}*\n{authors}\nISBN-{book['isbn']}",
            },
            "accessory": {
                "type": "image",
                "image_url": image_url,
                "alt_text": "Windsor Court Hotel thumbnail",
            },
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "選択", "emoji": True},
                    "value": book["isbn"],
                    "action_id": "select_book_action",
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Google Booksで見る",
                        "emoji": True,
                    },
                    "url": book["google_books_url"],
                    "action_id": "google_books_buttons_action",
                },
            ],
        },
    ]

    return block


def book_search_result_selected_modal(
    *,
    callback_id: str,
    private_metadata: str,
    book_search_result_modal_blocks,
    isbn: str,
):
    """
    選択ボタンが選択された状態の、本の検索結果モーダル

    Args:
        callback_id: モーダルのcallback_id
        private_metadata: モーダルのprivate_metadata
        book_search_result_modal_blocks: 以前の本の検索結果モーダルのblocks
        isbn: 選択された本のISBN
    """

    new_blocks = [
        x
        if x["type"] != "actions"
        else _selected_book(x)
        if x["elements"][0]["value"] == isbn
        else _unselected_book(x)
        for x in book_search_result_modal_blocks
    ]

    # Blocksで渡ってくるimageには余計なパラメータが付与されているため一旦削除して付け直す
    new_blocks = [x for x in new_blocks if x["type"] != "image"]
    new_blocks.insert(0, google_graphic())

    return {
        "type": "modal",
        "callback_id": callback_id,
        "private_metadata": private_metadata,
        "title": {
            "type": "plain_text",
            "text": "書籍の検索結果",
            "emoji": True,
        },
        "close": {"type": "plain_text", "text": "戻る", "emoji": True},
        "submit": {"type": "plain_text", "text": "決定", "emoji": True},
        "blocks": new_blocks,
    }


def _selected_book(item) -> dict[str, Any]:
    """
    ボタンが選択された本のblockを生成する
    """
    return {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": ":hand:選択中です",
                    "emoji": True,
                },
                "value": item["elements"][0]["value"],
                "action_id": "select_book_action",
                "style": "primary",
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Google Booksで見る",
                    "emoji": True,
                },
                "url": item["elements"][1]["url"],
                "action_id": "google_books_buttons_action",
            },
        ],
    }


def _unselected_book(item) -> dict[str, Any]:
    """
    ボタンが選択されていない本のblockを生成する
    """
    return {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "選択", "emoji": True},
                "value": item["elements"][0]["value"],
                "action_id": "select_book_action",
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Google Booksで見る",
                    "emoji": True,
                },
                "url": item["elements"][1]["url"],
                "action_id": "google_books_buttons_action",
            },
        ],
    }
