def home(
    *,
    see_more_recommended_book_action_id: str,
    read_review_action_id: str,
    post_review_action_id: str,
    user_info_action_id: str,
    review_count_all: int,
):
    """
    アプリホーム画面

    Args:
        see_more_recommended_book_action_id: 「詳しく見る」ボタンのaction_id
        read_review_action_id: 「レビューを閲覧する」ボタンのaction_id
        post_review_action_id: 「レビューを投稿する」ボタンのaction_id
        user_info_action_id: 「プロフィール」ボタンのaction_id
        review_count_all: 表示する「レビュー投稿数」
    """
    return {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "読書レビュー共有アプリ「Bee（Book Erabu Eiwa）」",
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
                    "text": "あなたにおすすめの本は...\n *「仕事ではじめる機械学習」* ",
                },
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "詳しく見る",
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
                        "text": f"*現在のレビュー投稿数 {review_count_all}件*",
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
        ],
    }
