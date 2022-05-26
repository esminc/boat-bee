from bee_slack_app.model.search import SearchedBook


def generate_book_recommend_model_view(callback_id: str, book: SearchedBook):
    """
    おすすめ本モーダル

    Args:
        callback_id: モーダルのcallback_id
        book: ブック
    """

    # TODO: 暫定で適当な画像をデフォルトに設定、S3に画像を置くようになったら自前の画像に差し替える
    dummy_url = (
        "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg"
    )
    image_url = book["image_url"] if book["image_url"] is not None else dummy_url
    authors = ", ".join(book["authors"])

    view = {
        "type": "modal",
        "callback_id": callback_id,
        "title": {"type": "plain_text", "text": "あなたへのおすすめ本"},
        "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{book['title']}*\n{authors}\nISBN-{book['isbn']}",
                },
                "accessory": {
                    "type": "image",
                    "image_url": image_url,
                    "alt_text": "An incredibly cute kitten.",
                },
            },
            {
                "type": "actions",
                "elements": [
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
            {
                "type": "image",
                "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
                "alt_text": "",
            },
        ],
    }
    return view
