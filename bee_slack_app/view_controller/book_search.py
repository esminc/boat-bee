import json

from bee_slack_app.service.book_search import search_book_by_title
from bee_slack_app.service.user_action import record_user_action
from bee_slack_app.view.book_search import (
    book_search_result_modal,
    book_search_result_selected_modal,
)
from bee_slack_app.view.common import simple_modal
from bee_slack_app.view.post_review import post_review_modal


# TODO: disable=too-many-statementsを取り消す
def book_search_controller(app):  # pylint: disable=too-many-statements
    @app.view("book_search_modal")
    def open_book_search_result_modal(ack, body):
        """
        検索結果のモーダルを開く
        """
        title = body["view"]["state"]["values"]["input_book_title"][
            "book_title_action"
        ]["value"]

        book_results = search_book_by_title(title)

        record_user_action(
            user_id=body["user"]["id"],
            action_name="book_search_modal",
            payload={"book_results": book_results},
        )

        if len(book_results) == 0:
            ack(
                response_action="push",
                view=simple_modal(title="検索結果", text="検索結果が0件でした"),
            )
            return
        book_result_summary = []

        for book_result in book_results:

            # ボタン選択時に書籍のデータを再利用するため情報を保持しておく
            # とりあえずはTitleとISBNを取得できれば良い
            # private_metadataに格納できる情報が3000文字なので最小限にする
            book_info = {
                "isbn": book_result["isbn"],
                "title": book_result["title"],
            }
            book_result_summary.append(book_info)

        # private_metadataに格納するために文字列に変換する
        private_metadata = json.dumps(book_result_summary)

        ack(
            response_action="push",
            view=book_search_result_modal(
                callback_id="book_search_result_modal",
                private_metadata=private_metadata,
                book_results=book_results,
            ),
        )

    @app.action("select_book_action")
    def handle_book_selected(ack, body, _, client):
        """
        検索結果画面で選択ボタンを選択した時に行う処理
        """

        private_metadata = body["view"]["private_metadata"]

        # private_metadataに格納していた情報を復元する
        search_result: list = json.loads(private_metadata)

        # private_metadataに選択情報が入っている場合は取り除く
        search_result = [x for x in search_result if x.get("isbn", None) is not None]

        isbn = body["actions"][0]["value"]
        title = [x for x in search_result if x["isbn"] == isbn][0]["title"]

        # private_metadataに選択情報を追加する
        selected_item = {"selected_title": title, "selected_isbn": isbn}
        search_result.append(selected_item)

        # ボタンの選択状態を更新する
        blocks = body["view"]["blocks"]

        client.views_update(
            view_id=body["container"]["view_id"],
            view=book_search_result_selected_modal(
                callback_id="book_search_result_modal",
                private_metadata=json.dumps(search_result),
                book_search_result_modal_blocks=blocks,
                isbn=isbn,
            ),
        )
        ack()

    @app.action("google_books_buttons_action")
    def handle_google_books_selected(ack, body, _, logger):
        """
        検索結果画面でGoogle Booksで見るボタンを押した時に行う処理

        何か処理する必要はないがackを返さないとエラーが発生するのでackのみ返す
        """
        ack()
        logger.info(body)

    @app.view("book_search_result_modal")
    def handle_submission(ack, body, _, __):
        """
        検索結果画面で決定ボタンを押した時に行う処理
        """

        # 通常のボタン押下状態はactionsには入ってこないためprivate_metadataで伝達する
        # private_metadataに格納していたCacheを文字列から復元する
        cache_list = body["view"]["private_metadata"]
        items: list = json.loads(cache_list)

        books = [x for x in items if x.get("selected_title", None) is not None]

        if len(books) == 0:
            ack(
                response_action="push",
                view=simple_modal(title="エラー", text="本が選択されていません"),
            )
            return

        blocks = body["view"]["blocks"]

        # 選択された本のbook_sectionとurlを、ISBNをもとに取得する (ハック的な対処なので注意)
        selected_book_section = None
        url = None

        for i, block in enumerate(blocks):
            if (
                "elements" in block
                and block["elements"][0]["value"] == books[0]["selected_isbn"]
            ):
                selected_book_section = blocks[i - 1]  # iは選択された本のaction blockのindex
                url = blocks[i]["elements"][1]["url"]

        if not selected_book_section or not url:
            record_user_action(
                user_id=body["user"]["id"],
                action_name="book_search_result_modal",
                status="fetch_book_data_error",
            )

            ack(
                response_action="push",
                view=simple_modal(title="エラー", text="本のデータ取得でエラーが発生しました"),
            )
            return

        record_user_action(
            user_id=body["user"]["id"],
            action_name="book_search_result_modal",
            payload={"selected_book_section": selected_book_section},
        )

        ack(
            response_action="push",
            view=post_review_modal(
                callback_id="post_review_modal",
                book_section=selected_book_section,
                url=url,
            ),
        )
