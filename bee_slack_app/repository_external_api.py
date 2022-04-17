import os
from typing import Optional, Tuple

import requests  # type: ignore


class _BookSearch:

    # 楽天API (BooksGenre/Search/)のURL/APP_AD
    url = "https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404"
    APPLICATION_ID = os.environ["RAKU_APP_ID"]

    def search_by_title(self, target_title: str) -> Tuple[int, dict[str, str]]:
        """
        タイトルから書籍を検索する

        Args:
            title : 検索したい書籍のタイトル（曖昧検索も可能）
        Returns:
            hits: 検索でヒットした件数
            dict: ヒットした書籍のタイトル(key)とISBN(value)の辞書形式データ
        """
        # URLのパラメータ
        param = {
            # 取得したアプリIDを設定する
            "applicationId": self.APPLICATION_ID,
            "keyword": target_title,
            "format": "json",
        }

        # APIを実行して結果を取得する
        result = requests.get(self.url, param)

        # jsonにデコードする
        json_result = result.json()

        # print(json_result)

        # 整形した結果を格納する辞書型変数を宣言
        dict_result = {}

        # 取得結果を1件ずつ取り出す
        for value in json_result["Items"]:
            item = value["Item"]

            # keyに「タイトル（title）」、valueに「ISBN（isbn）」を設定する
            dict_result[item["title"]] = item["isbn"]

        return json_result["hits"], dict_result

    def search_by_isbn(self, isbn: int) -> Tuple[bool, Optional[str]]:
        """
        ISBNから書籍を検索する

        Args:
            isbn : 検索したい書籍のISBN(13桁の数字、ハイフンなし)
        Returns:
            bool: 検索でヒットした（True）、ヒットしなかった（False）
            str:  ヒットした書籍のタイトル
        """
        # URLのパラメータ
        param = {
            # 取得したアプリIDを設定する
            "applicationId": self.APPLICATION_ID,
            "isbnjan": isbn,
            "format": "json",
        }

        # APIを実行して結果を取得する
        result = requests.get(self.url, param)

        # jsonにデコードする
        json_result = result.json()

        print(json_result)

        if json_result["hits"] != 1:
            return False, None

        return True, json_result["Items"][0]["Item"]["title"]


bookSearch = _BookSearch()


# Usage example
hits, titles = bookSearch.search_by_title("仕事ではじめる機械学習")

print(f"hits: {hits} \ntitles: \n  {titles}")


hits, title = bookSearch.search_by_isbn(9784873119472)

print(f"hits: {hits}\ntitle: {title}")
