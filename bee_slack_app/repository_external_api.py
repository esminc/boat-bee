import os
from typing import List, Optional, Tuple

import requests  # type: ignore


class _BookSearch:

    # 楽天API (BooksGenre/Search/)のURL/APP_AD
    url = "https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404"
    APPLICATION_ID = os.environ["RAKU_APP_ID"]

    def search_by_title(self, target_title: str) -> Tuple[int, List[dict[str, str]]]:
        """
        タイトルから書籍を検索する

        Args:
            title : 検索したい書籍のタイトル（曖昧検索も可能）
        Returns:
            hits: 検索でヒットした件数
            list: ヒットした書籍の辞書形式データをリストで格納する
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

        # 整形した結果を格納するリスト型変数を宣言
        list_result = []

        # 取得結果を1件ずつ取り出す
        for value in json_result["Items"]:
            _item = value["Item"]

            # 必要な情報を辞書に格納する
            dict_item = {
                "title": _item["title"],
                "isbn": _item["isbn"],
                "author": _item["author"],
            }
            list_result.append(dict_item)

        return json_result["hits"], list_result

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

        # print(json_result)

        if json_result["hits"] != 1:
            return False, None

        return True, json_result["Items"][0]["Item"]["title"]


bookSearch = _BookSearch()


# Usage example

print("===== search by title('仕事ではじめる') =====")

hits, items = bookSearch.search_by_title("仕事ではじめる")
print(f"hits: {hits}")
for item in items:
    print(f"title: {item['title']}  isbn: {item['isbn']}  author: {item['author']}")

print("===== search by isbn('9784873119472') =====")

hits, title = bookSearch.search_by_isbn(9784873119472)

print(f"hits: {hits}\ntitle: {title}")
