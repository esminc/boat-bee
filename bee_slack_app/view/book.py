def see_more_recommended_book_modal():
    """
    あなたへのおすすめ本モーダル
    """
    return {
        "type": "modal",
        "title": {"type": "plain_text", "text": "あなたへのおすすめ本", "emoji": True},
        "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "ごめんなさい :bow: \nここは未実装です!!\n\nみなさんのレビューがたまれば、\nそれを元に、あなたにおすすめの本を表示します!!",
                },
            }
        ],
    }
