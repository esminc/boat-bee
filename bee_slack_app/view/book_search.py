from bee_slack_app.model.search import SearchedBook


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
    blocks.append(
        {
            "type": "image",
            "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
            "alt_text": "",
        },
    )

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
    # TODO: 暫定で適当な画像をデフォルトに設定、S3に画像を置くようになったら自前の画像に差し替える
    dummy_url = (
        "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg"
    )

    author = ", ".join(book["author"])
    image_url = book["image_url"] if book["image_url"] is not None else dummy_url

    block = [
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{book['title']}*\n{author}\nISBN-{book['isbn']}",
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
                    "action_id": "select_buttons-action",
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Google Booksで見る",
                        "emoji": True,
                    },
                    "url": book["google_books_url"],
                    "action_id": "google_books_buttons-action",
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
    new_blocks.insert(
        0,
        {
            "type": "image",
            "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
            "alt_text": "",
        },
    )

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


def _selected_book(item):
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
                "action_id": "select_buttons-action",
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
                "action_id": "google_books_buttons-action",
            },
        ],
    }


def _unselected_book(item):
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
                "action_id": "select_buttons-action",
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Google Booksで見る",
                    "emoji": True,
                },
                "url": item["elements"][1]["url"],
                "action_id": "google_books_buttons-action",
            },
        ],
    }
