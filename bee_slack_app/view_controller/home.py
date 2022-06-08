import json
from logging import getLogger
from typing import Any, Optional, TypedDict

from bee_slack_app.service.suggested import get_is_interested, add_suggested
from bee_slack_app.service import (
    book_service,
    recommend_service,
    review_service,
    user_action_service,
    user_service,
)
from bee_slack_app.utils.datetime import parse
from bee_slack_app.view.home import home

BOOK_NUMBER_PER_PAGE = 20


def home_controller(app):  # pylint: disable=too-many-statements
    @app.event("app_home_opened")
    def update_home_view(ack, event, client):
        ack()

        logger = getLogger(__name__)

        reviews = review_service.get_review_all()

        total_review_count = len(reviews) if reviews else 0
        recommend_timestamp = parse(recommend_service.created_at())

        user_action_service.record_user_action(
            user_id=event["user"],
            action_name="app_home_opened",
            payload={"total_review_count": total_review_count},
        )

        logger.info({"total_review_count": total_review_count})

        user = user_service.get_user(event["user"])
        user_name = f"{user['user_name']}さん" if user is not None else "あなた"

        recommended_books = recommend_service.recommend(user)

        # 興味ありボタンの状態をDBから取り出す
        button_status_list = []
        for recommended_book in recommended_books:
            interested_status: Optional[bool] = get_is_interested(
                user_id=event["user"],
                isbn=recommended_book[0]["isbn"],
                ml_model=recommended_book[1],
            )
            button_status_list.append(
                False if interested_status is None else interested_status
            )
        print("recommended_status=", button_status_list)

        books_params = None
        metadata_str = ""

        books = book_service.get_books(limit=BOOK_NUMBER_PER_PAGE, keys=[])

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
                list_user_posted_review_action_id="list_user_posted_review_action",
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

        reviews = review_service.get_review_all()

        total_review_count = len(reviews) if reviews else 0
        recommend_timestamp = parse(recommend_service.created_at())

        user = user_service.get_user(user_id)
        user_name = f"{user['user_name']}さん" if user is not None else "あなた"

        recommended_books = recommend_service.recommend(user)

        button_status_list = [False, False, False]

        books_params = None
        metadata_str = ""

        books = book_service.get_books(
            limit=BOOK_NUMBER_PER_PAGE, keys=metadata_dict["keys"]
        )

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
                list_user_posted_review_action_id="list_user_posted_review_action",
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

        reviews = review_service.get_review_all()

        total_review_count = len(reviews) if reviews else 0
        recommend_timestamp = parse(recommend_service.created_at())

        user = user_service.get_user(user_id)
        user_name = f"{user['user_name']}さん" if user is not None else "あなた"

        recommended_books = recommend_service.recommend(user)

        # 興味ありボタンの状態をDBから取り出す
        button_status_list = []
        for recommended_book in recommended_books:
            interested_status: Optional[bool] = get_is_interested(
                user_id=user_id,
                isbn=recommended_book[0]["isbn"],
                ml_model=recommended_book[1],
                # print("print_interested=",str(interested_status))
            )
            button_status_list.append(
                False if interested_status is None else interested_status
            )
        print("recommended_status=", button_status_list)

        metadata_dict = _PrivateMetadataConvertor.to_dict(
            private_metadata=private_metadata
        )

        books_params = None
        metadata_str = ""

        books = book_service.get_books_before(
            limit=BOOK_NUMBER_PER_PAGE, keys=metadata_dict["keys"]
        )

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
                list_user_posted_review_action_id="list_user_posted_review_action",
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

        reviews = review_service.get_review_all()

        total_review_count = len(reviews) if reviews else 0
        recommend_timestamp = parse(recommend_service.created_at())

        logger.info({"total_review_count": total_review_count})

        user = user_service.get_user(body["user"]["id"])
        user_name = f"{user['user_name']}さん" if user is not None else "あなた"

        recommended_books = recommend_service.recommend(user)

        # 興味ありボタンの状態をDBから取り出す
        button_status_list = []
        for recommended_book in recommended_books:
            interested_status: Optional[bool] = get_is_interested(
                user_id=body["user"]["id"],
                isbn=recommended_book[0]["isbn"],
                ml_model=recommended_book[1],
            )
            button_status_list.append(
                False if interested_status is None else interested_status
            )
        print("recommended_status=", button_status_list)

        books_params = None
        metadata_str = ""

        books = book_service.get_books(limit=BOOK_NUMBER_PER_PAGE, keys=[])

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
        print("recommended_status_write=", button_status_list)


class _PrivateMetadataConvertor:
    class _MetadataDict(TypedDict):
        keys: Any

    @staticmethod
    def to_private_metadata(*, keys: Any) -> str:
        return json.dumps({"keys": keys})

    @staticmethod
    def to_dict(*, private_metadata: str) -> _MetadataDict:
        return json.loads(private_metadata)
