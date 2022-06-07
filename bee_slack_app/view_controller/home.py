import json
from logging import getLogger
from typing import Any, TypedDict

from bee_slack_app.service.book import get_books, get_books_before
from bee_slack_app.service.recommend import created_at, recommend
from bee_slack_app.service.review import get_review_all
from bee_slack_app.service.user import get_user
from bee_slack_app.service.user_action import record_user_action
from bee_slack_app.utils.datetime import parse
from bee_slack_app.view.home import home

BOOK_NUMBER_PER_PAGE = 20


def home_controller(app):  # pylint: disable=too-many-statements
    @app.event("app_home_opened")
    def update_home_view(ack, event, client):
        ack()

        logger = getLogger(__name__)

        reviews = get_review_all()

        total_review_count = len(reviews) if reviews else 0
        recommend_timestamp = parse(created_at())

        record_user_action(
            user_id=event["user"],
            action_name="app_home_opened",
            payload={"total_review_count": total_review_count},
        )

        logger.info({"total_review_count": total_review_count})

        user = get_user(event["user"])
        user_name = f"{user['user_name']}さん" if user is not None else "あなた"

        recommended_books = recommend(user)

        # TODO: ボタン状態はDBから読み出す
        # とりあえず今は固定値で始める
        # button_status_list = [False, False, False]
        button_status_list = []
        print("recommended_user=", event["user"])
        for recommended_book in recommended_books:
            print("recommended_isbn=", recommended_book[0]["isbn"])
            print("recommended_ml_model=", recommended_book[1])
            button_status_list.append(False)
        print("recommended_status=", button_status_list)

        books_params = None
        metadata_str = ""

        books = get_books(limit=BOOK_NUMBER_PER_PAGE, keys=[])

        logger.info({"books": books})

        if books:
            books_params = {
                "books": books.get("items"),
                "show_move_to_back": False,
                "show_move_to_next": books.get("has_next"),
            }

            metadata_str = _PrivateMetadataConvertor.to_private_metadata(
                keys=books.get("keys")
            )

        client.views_publish(
            user_id=event["user"],
            view=home(
                suggested_callback_id="suggested_button_modal",
                button_status_list=button_status_list,
                post_review_action_id="post_review_action",
                recommended_books=recommended_books,
                user_info_action_id="user_info_action",
                total_review_count=total_review_count,
                user_name=user_name,
                recommend_timestamp=recommend_timestamp,
                books_params=books_params,
                private_metadata=metadata_str,
            ),
        )

    @app.action("home_move_to_next_action")
    def home_move_to_next_action(ack, client, body):  # pylint: disable=too-many-locals
        """
        ホーム画面で「次へ」を押下されたときの処理
        """
        ack()

        logger = getLogger(__name__)

        user_id = body["user"]["id"]

        private_metadata = body["view"]["private_metadata"]

        metadata_dict = _PrivateMetadataConvertor.to_dict(
            private_metadata=private_metadata
        )

        reviews = get_review_all()

        total_review_count = len(reviews) if reviews else 0
        recommend_timestamp = parse(created_at())

        user = get_user(user_id)
        user_name = f"{user['user_name']}さん" if user is not None else "あなた"

        recommended_books = recommend(user)

        button_status_list = [False, False, False]

        books_params = None
        metadata_str = ""

        books = get_books(limit=BOOK_NUMBER_PER_PAGE, keys=metadata_dict["keys"])

        logger.info({"books": books})

        if books:
            books_params = {
                "books": books.get("items"),
                "show_move_to_back": True,
                "show_move_to_next": books.get("has_next"),
            }

            metadata_str = _PrivateMetadataConvertor.to_private_metadata(
                keys=books.get("keys")
            )

        client.views_publish(
            user_id=user_id,
            view=home(
                suggested_callback_id="suggested_button_modal",
                button_status_list=button_status_list,
                post_review_action_id="post_review_action",
                recommended_books=recommended_books,
                user_info_action_id="user_info_action",
                total_review_count=total_review_count,
                user_name=user_name,
                recommend_timestamp=recommend_timestamp,
                books_params=books_params,
                private_metadata=metadata_str,
            ),
        )

    @app.action("home_move_to_back_action")
    def home_move_to_back_action(ack, client, body):  # pylint: disable=too-many-locals
        """
        ホーム画面で「前へ」を押下されたときの処理
        """
        ack()

        logger = getLogger(__name__)

        user_id = body["user"]["id"]

        private_metadata = body["view"]["private_metadata"]

        reviews = get_review_all()

        total_review_count = len(reviews) if reviews else 0
        recommend_timestamp = parse(created_at())

        user = get_user(user_id)
        user_name = f"{user['user_name']}さん" if user is not None else "あなた"

        recommended_books = recommend(user)

        button_status_list = [False, False, False]

        metadata_dict = _PrivateMetadataConvertor.to_dict(
            private_metadata=private_metadata
        )

        books_params = None
        metadata_str = ""

        books = get_books_before(limit=BOOK_NUMBER_PER_PAGE, keys=metadata_dict["keys"])

        logger.info({"books": books})

        if books:
            books_params = {
                "books": books.get("items"),
                "show_move_to_back": not books.get("is_move_to_first"),
                "show_move_to_next": True,
            }

            metadata_str = _PrivateMetadataConvertor.to_private_metadata(
                keys=books.get("keys")
            )

        client.views_publish(
            user_id=user_id,
            view=home(
                suggested_callback_id="suggested_button_modal",
                button_status_list=button_status_list,
                post_review_action_id="post_review_action",
                recommended_books=recommended_books,
                user_info_action_id="user_info_action",
                total_review_count=total_review_count,
                user_name=user_name,
                recommend_timestamp=recommend_timestamp,
                books_params=books_params,
                private_metadata=metadata_str,
            ),
        )

    @app.action("button_switch_action")
    def handle_updete_button_action(
        ack, body, client
    ):  # pylint: disable=too-many-locals

        ack()
        logger = getLogger(__name__)

        reviews = get_review_all()

        total_review_count = len(reviews) if reviews else 0
        recommend_timestamp = parse(created_at())

        logger.info({"total_review_count": total_review_count})

        user = get_user(body["user"]["id"])
        user_name = f"{user['user_name']}さん" if user is not None else "あなた"

        recommended_books = recommend(user)

        books_params = None
        metadata_str = ""

        books = get_books(limit=BOOK_NUMBER_PER_PAGE, keys=[])

        logger.info({"books": books})

        if books:
            books_params = {
                "books": books.get("items"),
                "show_move_to_back": False,
                "show_move_to_next": books.get("has_next"),
            }

            metadata_str = _PrivateMetadataConvertor.to_private_metadata(
                keys=books.get("keys")
            )

        # private_metadataに格納していた情報を復元する
        private_metadata = body["view"]["private_metadata"]
        button_info = json.loads(private_metadata)
        button_status_list = button_info["interested"]

        # どのボタンが押されたか判定する
        # valueにはstrしか格納できないためintに戻して利用する
        button = int(body["actions"][0]["value"])

        # 押されたボタンを反転させる
        button_status_list[button] = not button_status_list[button]

        # 興味ありボタンの表示を切り替える
        modal_view = home(
            suggested_callback_id="suggested_button_modal",
            button_status_list=button_status_list,
            post_review_action_id="post_review_action",
            recommended_books=recommended_books,
            user_info_action_id="user_info_action",
            total_review_count=total_review_count,
            user_name=user_name,
            recommend_timestamp=recommend_timestamp,
            books_params=books_params,
            private_metadata=metadata_str,
        )
        client.views_update(
            view_id=body["container"]["view_id"],
            view=modal_view,
        )

        # TODO: 最新のボタン状態をDBに格納する
        print("recommended_status=", button_status_list)


class _PrivateMetadataConvertor:
    class _MetadataDict(TypedDict):
        keys: Any

    @staticmethod
    def to_private_metadata(*, keys: Any) -> str:
        return json.dumps({"keys": keys})

    @staticmethod
    def to_dict(*, private_metadata: str) -> _MetadataDict:
        return json.loads(private_metadata)
