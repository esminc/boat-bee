import ipadic
import MeCab

from . import stopwords

wakati = MeCab.Tagger(ipadic.MECAB_ARGS)


def parse_to_words(target: str) -> list[str]:

    parsed = wakati.parse(target)

    parsed_lines = parsed.split("\n")

    parsed_words = []

    for parsed_line in parsed_lines:

        parsed_words.append(parsed_line.split("\t"))

    # 名詞のみを取り出す
    words = []
    for parsed_word in parsed_words:

        if len(parsed_word) > 1 and "名詞" in parsed_word[1]:
            words.append(parsed_word[0])

    # ストップワードを除去する
    clean_words = stopwords.remove_stopword(words)

    return clean_words
