import os
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

    def search_rakuten_by_isbn(self, isbn: int) -> Tuple[bool, Optional[str]]:
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

    def search_google_by_title(
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
            # "isbn": 9784873119472
            "q": f"intitle:{target_title}",
            "Country": "JP",
        }

        # APIを実行して結果を取得する
        # result = requests.get("https://www.googleapis.com/books/v1/volumes?q=%E4%BB%95%E4%BA%8B")
        json_result = requests.get(self.base_url_google, param).json()

        _hits = json_result["totalItems"]

        print(f"hits: {_hits}")

        # 整形した結果を格納するリスト型変数を宣言
        list_result = []

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
                "author": _item["volumeInfo"]["authors"],
            }
            list_result.append(dict_item)

        return _hits, list_result

    def search_google_by_isbn(self, isbn: int) -> Tuple[bool, Optional[str]]:
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
            "q": f"isbn:{isbn}",
            "Country": "JP",
        }

        # APIを実行して結果を取得する
        json_result = requests.get(self.base_url_google, param).json()

        if json_result["totalItems"] != 1:
            return False, None

        return True, json_result["items"][0]["volumeInfo"]["title"]

bookSearch = _BookSearch()


# Usage example

print("===== search rakuten by title('仕事ではじめる') =====")

hits, items = bookSearch.search_rakuten_by_title("仕事ではじめる")
print(f"hits: {hits}")
for item in items:
    print(f"title: {item['title']}  isbn: {item['isbn']}  author: {item['author']}")

print("===== search rakuten by isbn('9784873119472') =====")

hits, title = bookSearch.search_rakuten_by_isbn(9784873119472)

print(f"hits: {hits}\ntitle: {title}")

print("===== search google by title('仕事ではじめる') =====")
hits, items = bookSearch.search_google_by_title("仕事ではじめる")

print(f"hits: {hits}")
for item in items:
    print(f"title: {item['title']}  isbn: {item['isbn']}  author: {item['author']}")

print("===== search google by isbn('9784873119472') =====")

hits, title = bookSearch.search_google_by_isbn(9784873119472)

print(f"hits: {hits}\ntitle: {title}")
