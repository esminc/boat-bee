from typing import Optional

import requests  # type: ignore


class GoogleBooksRepository:
    def __init__(self):
        # Google API
        self.base_url_google = "https://www.googleapis.com/books/v1/volumes"

    def search_book_by_title(self, title: str) -> list[dict[str, str]]:
        """
        タイトルから書籍を検索する

        Args:
            title : 検索したい書籍のタイトル（曖昧検索も可能）
        Returns:
            list: ヒットした書籍の辞書形式データをリストで格納する
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
                "author": _item["volumeInfo"].get("authors", "No Authoer"),
                "google_books_url": _item["volumeInfo"]["infoLink"],
                "image_url": image_url,
            }
            list_result.append(dict_item)

        return list_result

    def search_book_by_isbn(self, isbn: str) -> Optional[dict[str, str]]:
        """
        ISBNから書籍を検索する

        Args:
            isbn : 検索したい書籍のISBN(13桁の数字、ハイフンなし)
        Returns:
            Optional[dict[str, str]]  : ヒットした書籍の情報を辞書形式で返す
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

        image_url = self._get_image_url(_item)

        # 必要な情報を辞書に格納する
        dict_info = {
            "title": _item["volumeInfo"]["title"],
            "isbn": isbn,
            "author": _item["volumeInfo"].get("authors", "No Authoer"),
            "google_books_url": _item["volumeInfo"]["infoLink"],
            "image_url": image_url,
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
