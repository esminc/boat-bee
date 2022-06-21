import json
from typing import Any, Optional

import requests  # type: ignore


class GoogleBooksRepository:
    def __init__(self):
        # Google API
        self.base_url_google = "https://www.googleapis.com/books/v1/volumes"

    def search_book_by_title(self, title: str) -> list[dict[str, Any]]:
        """
        タイトルから書籍を検索する

        Args:
            title : 検索したい書籍のタイトル（曖昧検索も可能）
        Returns:
            list[dict[str, Any]]  : ヒットした書籍の情報を辞書のリスト形式で返す
                                    ヒットしなかった場合は空のリストを返す
        """

        # URLのパラメータ
        param = {
            "q": f"intitle:{title}",
            "Country": "JP",
        }

        # APIを実行して結果を取得する
        json_result = requests.get(self.base_url_google, param).json()

        # 整形した結果を格納するリスト型変数を宣言
        list_result: list[dict[str, str]] = []

        # ヒットしなかった場合はJSONにItemsが含まれないのですぐに空のListを返す
        _hits = json_result["totalItems"]
        if _hits == 0:
            return list_result

        # 取得結果を1件ずつ取り出す
        for _item in json_result["items"]:

            # ISBN13を取り出す
            isbn_list = _item["volumeInfo"].get("industryIdentifiers")
            if not isbn_list:
                continue
            isbn_13_list = [x for x in isbn_list if x["type"] == "ISBN_13"]

            # ISBN13がない場合は検索結果から除外する
            if len(isbn_13_list) != 1:
                continue

            isbn_13 = isbn_13_list[0]["identifier"]

            image_url = self._get_image_url(_item)

            # 必要な情報を辞書に格納する
            dict_item = {
                "title": _item["volumeInfo"]["title"],
                "isbn": isbn_13,
                "authors": _item["volumeInfo"].get("authors", ["No Author"]),
                "google_books_url": _item["volumeInfo"]["infoLink"],
                "image_url": image_url,
                "description": _item["volumeInfo"].get("description", ["-"]),
            }
            list_result.append(dict_item)

        # 辞書のリストから重複を取り除く
        # see: https://qiita.com/kilo7998/items/184ed972571b2e202b40
        # list_result = list(map(json.loads, set(map(json.dumps, list_result))))

        return list_result

    def search_book_by_isbn(self, isbn: str) -> Optional[dict[str, Any]]:
        """
        ISBNから書籍を検索する

        Args:
            isbn : 検索したい書籍のISBN(13桁の数字、ハイフンなし)
        Returns:
            Optional[dict[str, Any]]  : ヒットした書籍の情報を辞書形式で返す
                                        ヒットしなかった場合はNoneを返す
        """

        # URLのパラメータ
        param = {
            "q": f"isbn:{isbn}",
            "Country": "JP",
        }

        # APIを実行して結果を取得する
        json_result = requests.get(self.base_url_google, param).json()

        if json_result["totalItems"] == 0:
            return None

        _item = json_result["items"][0]

        image_url = self._get_image_url(_item)

        # 必要な情報を辞書に格納する
        dict_info = {
            "title": _item["volumeInfo"]["title"],
            "isbn": isbn,
            "authors": _item["volumeInfo"].get("authors", ["No Author"]),
            "google_books_url": _item["volumeInfo"]["infoLink"],
            "image_url": image_url,
            "description": _item["volumeInfo"].get("description", "-"),
        }

        return dict_info

    @staticmethod
    def _get_image_url(_item):
        if (
            _item["volumeInfo"].get("imageLinks") is not None
            and _item["volumeInfo"].get("imageLinks").get("thumbnail") is not None
        ):
            image_url = _item["volumeInfo"]["imageLinks"]["thumbnail"]
        else:
            image_url = None
        return image_url
