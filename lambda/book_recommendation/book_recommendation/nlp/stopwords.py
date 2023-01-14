import requests

URL = "http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt"


def fetch_stopwords_from_slothlib() -> list[str]:

    return requests.get(URL).text.split("\r\n")


def remove_stopword(words: list[str]) -> list[str]:

    return [word for word in words if word not in stop_words]


stop_words = []
stop_words.extend(
    [
        "方",
        "方法",
        "こと",
        "ため",
        "人",
        "性",
        "何",
        "等",
        "化",
        "場合",
        "点",
        "時",
        "工夫",
        "様",
        "中",
        "とき",
        "ところ",
        "もの",
        "それ",
        "書",
        "側",
        "内",
        "際",
    ]
)
stop_words.extend(["以下", "20", "年", "M"])
stop_words.extend(["内容", "作成"])
stop_words.extend(list("0123456789"))
stop_words.extend(list("０１２３４５６７８９"))
stop_words.extend(["．", "どこ", "以外", "つ", "目", "さん"])
stop_words.extend(
    [
        "あ",
        "い",
        "う",
        "え",
        "お",
        "か",
        "き",
        "く",
        "け",
        "こ",
        "さ",
        "し",
        "す",
        "せ",
        "そ",
        "た",
        "ち",
        "つ",
        "て",
        "と",
        "な",
        "に",
        "ぬ",
        "ね",
        "の",
        "は",
        "ひ",
        "ふ",
        "へ",
        "ほ",
        "ま",
        "み",
        "む",
        "め",
        "も",
        "や",
        "ゆ",
        "よ",
        "ら",
        "り",
        "る",
        "れ",
        "ろ",
        "わ",
        "を",
        "ん",
    ]
)
stop_words.extend(
    [
        "が",
        "ぎ",
        "ぐ",
        "げ",
        "ご",
        "ざ",
        "じ",
        "ず",
        "ぜ",
        "ぞ",
        "だ",
        "ぢ",
        "づ",
        "で",
        "ど",
        "ば",
        "び",
        "ぶ",
        "べ",
        "ぼ",
    ]
)
stop_words.extend(fetch_stopwords_from_slothlib())
