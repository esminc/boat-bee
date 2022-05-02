"""
DBのスコアを引数として受け取り、モーダルに表示する文言を戻り値に設定する
"""


class ViewScore:
    def __init__(self):
        self.score_for_me_value = {
            "5": "とても良い",
            "4": "良い",
            "3": "普通",
            "2": "悪い",
            "1": "とても悪い",
        }
        self.score_for_others_value = {
            "5": "とてもおすすめ",
            "4": "おすすめ",
            "3": "普通",
            "2": "おすすめしない",
            "1": "絶対におすすめしない",
        }

    def score_for_me(self, score_key: str) -> str:
        return self.score_for_me_value[score_key]

    def score_for_others(self, score_key: str) -> str:
        return self.score_for_others_value[score_key]
