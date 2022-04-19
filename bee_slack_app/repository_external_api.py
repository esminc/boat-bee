import os
import sys
from typing import List, Optional, Tuple

import requests  # type: ignore


class _BookSearch:

    # 楽天API (BooksGenre/Search/)のURL/APP_AD
    url = "https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404"
    APPLICATION_ID = os.environ["RAKU_APP_ID"]

    # Google API
    base_url_google = "https://www.googleapis.com/books/v1/volumes"

    def search_rakuten_by_title(
        self, target_title: str
    ) -> Tuple[int, List[dict[str, str]]]:
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

    def search_rakuten_by_isbn(self, isbn: str) -> Tuple[int, Optional[dict[str, str]]]:
        """
        ISBNから書籍を検索する

        Args:
            isbn : 検索したい書籍のISBN(13桁の数字、ハイフンなし)
        Returns:
            bool: 検索でヒットした（True）、ヒットしなかった（False）
            dict_info:  ヒットした書籍の情報を辞書形式で返す
        """

        if len(isbn) != 13:
            print(f"ERROR: isbn should be 13 digits but [{len(isbn)}]")
            return False, None

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

        if json_result["count"] != 1:
            return False, None

        _item = json_result["Items"][0]["Item"]

        # 必要な情報を辞書に格納する
        dict_info = {
            "title": _item["title"],
            "author": _item["author"],
        }

        return True, dict_info

    def search_google_by_title(
        self, target_title: str
    ) -> List[dict[str, str]]:
        """
        タイトルから書籍を検索する

        Args:
            title : 検索したい書籍のタイトル（曖昧検索も可能）
        Returns:
            list: ヒットした書籍の辞書形式データをリストで格納する
        """

        # URLのパラメータ
        param = {
            # "isbn": 9784873119472
            "q": f"intitle:{target_title}",
            "Country": "JP",
        }

        # APIを実行して結果を取得する
        # result = requests.get("https://www.googleapis.com/books/v1/volumes?q=%E4%BB%95%E4%BA%8B")
        json_result = requests.get(self.base_url_google, param).json()


        # 整形した結果を格納するリスト型変数を宣言
        list_result: List[dict[str, str]] = []

        # ヒットしなかった場合はJSONにItemsが含まれないのですぐに空のListを返す
        _hits = json_result["totalItems"]
        if _hits == 0:
            return list_result

        # 取得結果を1件ずつ取り出す
        for _item in json_result["items"]:

            # ISBN13を取り出す
            isbn_list = _item["volumeInfo"]["industryIdentifiers"]
            isbn_13_list = [x for x in isbn_list if x["type"] == "ISBN_13"]

            # ISBN13がない場合は検索結果から除外する
            if len(isbn_13_list) != 1:
                continue

            isbn_13 = isbn_13_list[0]["identifier"]

            # 必要な情報を辞書に格納する
            dict_item = {
                "title": _item["volumeInfo"]["title"],
                "isbn": isbn_13,
                "author": _item["volumeInfo"].get("authors", "No Authoer"),
            }
            list_result.append(dict_item)

        return list_result

    def search_google_by_isbn(self, isbn: str) -> Optional[dict[str, str]]:
        """
        ISBNから書籍を検索する

        Args:
            isbn : 検索したい書籍のISBN(13桁の数字、ハイフンなし)
        Returns:
            dict_info : ヒットした書籍の情報を辞書形式で返す
                        ヒットしなかった場合はNoneを返す
        """

        # URLのパラメータ
        param = {
            "q": f"isbn:{isbn}",
            "Country": "JP",
        }

        # APIを実行して結果を取得する
        json_result = requests.get(self.base_url_google, param).json()

        if json_result["totalItems"] != 1:
            return None

        _item = json_result["items"][0]

        # 必要な情報を辞書に格納する
        dict_info = {
            "title": _item["volumeInfo"]["title"],
            "author": _item["volumeInfo"].get("authors", "No Authoer"),
        }

        return dict_info


bookSearch = _BookSearch()


# Usage example
args = sys.argv
given_title = args[1]
given_isbn = args[2]

print("----------------------------------------------------------------------------")
print(f"args: {args}")
print(f"===== search rakuten by title({given_title}) =====")

hits, items = bookSearch.search_rakuten_by_title(given_title)
print(f"hits: {hits}")
for item in items:
    print(f"title: {item['title']}  isbn: {item['isbn']}  author: {item['author']}")

print(f"===== search rakuten by isbn({given_isbn}) =====")

hits, informations = bookSearch.search_rakuten_by_isbn(given_isbn)

print(f"hits: {hits}\ntitle: {informations}")

print(f"===== search google by title({given_title}) =====")
items = bookSearch.search_google_by_title(given_title)

print(f"hits: {len(items)}")
for item in items:
    print(f"title: {item['title']}  isbn: {item['isbn']}  author: {item['author']}")

print(f"===== search google by isbn({given_isbn}) =====")

info = bookSearch.search_google_by_isbn(given_isbn)
print(f"info: {info}")
