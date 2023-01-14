from typing import Optional, TypedDict

from bee_slack_app.model import Book, RecommendBook
from bee_slack_app.view.common import book_section, google_graphic


class BooksParam(TypedDict):
    books: list[Book]
    show_move_to_back: bool
    show_move_to_next: bool


def home(  # pylint: disable=too-many-locals
    *,
    recommended_books: Optional[list[RecommendBook]],
    post_review_action_id: str,
    list_user_posted_review_action_id: str,
    user_info_action_id: str,
    total_review_count: int,
    user_name: str,
    recommend_timestamp: str,
    books_params: Optional[BooksParam] = None,
    private_metadata: str = "",
):  # pylint: disable=too-many-locals
    """
    アプリホーム画面

    Args:
        recommended_books: 「おすすめ本」のデータ
        post_review_action_id: 「レビューを投稿する」ボタンのaction_id
        list_user_posted_review_action_id: 「レビューを投稿したユーザ」ボタンのaction_id
        user_info_action_id: 「プロフィール」ボタンのaction_id
        total_review_count: 表示する「レビュー投稿数」
        user_name:表示する「ユーザ名」
        recommend_timestamp:MLのjsonファイルを作成した日時
        books_param: 「レビューが投稿されている本」のデータ
        private_metadata: private_metadata
    """
    recommended_book_sections = []
    if recommended_books:
        for recommended_book in recommended_books:

            recommended_book_sections.append(
                book_section(
                    title=recommended_book["title"],
                    author=recommended_book["author"],
                    isbn=recommended_book["isbn"],
                    url=recommended_book["url"],
                    image_url=recommended_book["image_url"],
                ),
            )

            suggested_button_value = {
                "isbn": recommended_book["isbn"],
                "ml_model": recommended_book["ml_model"],
                "interested": recommended_book["interested"],
            }
            recommended_book_sections.append(create_button(suggested_button_value))
    else:
        recommended_book_sections.append(
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "おすすめ本を見るには、レビュー投稿をお願いします :pray:",
                    "emoji": True,
                },
            },
        )

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
                    "text": f"{user_name}へのおすすめ本",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*最新の推薦データ* : {recommend_timestamp}",
                },
            },
        ],
    }
    view["blocks"].extend(recommended_book_sections)  # type: ignore

    following_blocks = [
        {"type": "divider"},
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
                        "text": "レビューを投稿する :memo:",
                        "emoji": True,
                    },
                    "value": "dummy_value",
                    "action_id": post_review_action_id,
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "レビューを投稿したユーザ",
                        "emoji": True,
                    },
                    "value": "dummy_value",
                    "action_id": list_user_posted_review_action_id,
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
        google_graphic(),
    ]

    view["blocks"].extend(following_blocks)  # type: ignore

    book_sections = []

    move_buttons = {"type": "actions", "elements": []}

    if books_params:

        for book in books_params["books"]:

            book_sections.append(
                book_section(
                    title=book["title"],
                    author=book["author"],
                    isbn=book["isbn"],
                    url=book["url"],
                    image_url=book["image_url"],
                ),
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


def create_button(suggested_book_value: dict) -> dict:
    button_name = "興味あり❤️" if suggested_book_value["interested"] else "興味なし🤍"
    return {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": button_name,
                    "emoji": True,
                },
                "value": f'{suggested_book_value["isbn"]}#{suggested_book_value["ml_model"]}',
                "action_id": "button_switch_action",
            },
            {  # type: ignore
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "この本のレビューを見る",
                    "emoji": True,
                },
                "value": suggested_book_value["isbn"],
                "action_id": "read_review_of_book_action",
            },
        ],
    }
