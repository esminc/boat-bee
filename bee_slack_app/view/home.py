from typing import Optional, TypedDict

from bee_slack_app.model.book import Book


class BooksParam(TypedDict):
    books: list[Book]
    show_move_to_back: bool
    show_move_to_next: bool


def home(
    *,
    see_more_recommended_book_action_id: str,
    read_review_action_id: str,
    post_review_action_id: str,
    user_info_action_id: str,
    total_review_count: int,
    books_params: Optional[BooksParam] = None,
    private_metadata: str = "",
):
    """
    アプリホーム画面

    Args:
        see_more_recommended_book_action_id: 「詳しく見る」ボタンのaction_id
        read_review_action_id: 「レビューを閲覧する」ボタンのaction_id
        post_review_action_id: 「レビューを投稿する」ボタンのaction_id
        user_info_action_id: 「プロフィール」ボタンのaction_id
        total_review_count: 表示する「レビュー投稿数」
        books_param: 「レビューが投稿されている本」のデータ
        private_metadata: private_metadata
    """

    view = {
        "type": "home",
        "private_metadata": private_metadata,
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "読書レビュー共有アプリ「Bee（Book Erabu Eiwa）」 :bee:",
                    "emoji": True,
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*読んだ本のレビューを投稿して、データ蓄積に協力お願いします* ",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Beeは、FDOが開発・提供する、本のレビュー共有アプリです。\n仕事で役立った本のレビューを投稿・共有できます。\nデータがたまればたまるほど、AIはより賢くなりあなたに合ったおすすめの本をお伝えすることができます。\n書籍購入制度で購入した本などのレビューを投稿してみましょう！！。",
                },
            },
            {"type": "divider"},
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "あなたへのおすすめ本",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "あなたにおすすめの本は... ",
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "おすすめの本を確認する",
                            "emoji": True,
                        },
                        "value": "dummy_value",
                        "action_id": see_more_recommended_book_action_id,
                    }
                ],
            },
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "本のレビュー", "emoji": True},
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*現在のレビュー投稿数 {total_review_count}件*",
                    },  # type:ignore
                ],
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "レビューを閲覧する :eyes:",
                            "emoji": True,
                        },
                        "value": "dummy_value",
                        "action_id": read_review_action_id,
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "レビューを投稿する :memo:",
                            "emoji": True,
                        },
                        "value": "dummy_value",
                        "action_id": post_review_action_id,
                    },
                ],
            },
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "ユーザ情報", "emoji": True},
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "プロフィール",
                            "emoji": True,
                        },
                        "value": "dummy_value",
                        "action_id": user_info_action_id,
                    },
                ],
            },
            {"type": "divider"},
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "レビューが投稿されている本",
                    "emoji": True,
                },
            },
            {
                "type": "image",
                "image_url": "https://developers.google.com/maps/documentation/images/powered_by_google_on_white.png",
                "alt_text": "Google Logo",
            },
        ],
    }

    book_sections = []

    move_buttons = {"type": "actions", "elements": []}

    if books_params:

        for book in books_params["books"]:

            book_sections.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{book['title']}*\n{book['author']}\nISBN-{book['isbn']}\n<{book['url']}|Google Booksで見る>",
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": book["image_url"],
                        "alt_text": book["title"],
                    },
                },
            )

            book_sections.append(
                {
                    "type": "actions",
                    "elements": [
                        {  # type: ignore
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "この本のレビューを見る",
                                "emoji": True,
                            },
                            "value": book["isbn"],
                            "action_id": "read_review_of_book_action",
                        }
                    ],
                },
            )

        if books_params["show_move_to_back"]:
            move_buttons["elements"] = [
                {  # type: ignore
                    "type": "button",
                    "text": {"type": "plain_text", "text": "前へ"},
                    "action_id": "home_move_to_back_action",
                }
            ]

        if books_params["show_move_to_next"]:
            move_buttons["elements"] = move_buttons["elements"] + [  # type: ignore
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "次へ"},
                    "action_id": "home_move_to_next_action",
                }
            ]

        if bool(move_buttons["elements"]):
            book_sections.append(move_buttons)  # type: ignore
    else:
        book_sections.append(
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "本の取得に失敗しました :expressionless:",
                    "emoji": True,
                },
            },
        )

    view["blocks"].extend(book_sections)  # type: ignore

    return view
