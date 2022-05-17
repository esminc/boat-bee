from typing import Optional

from bee_slack_app.model.user import User
from bee_slack_app.service.user import add_user, get_user
from bee_slack_app.view.user import user_profile_modal


def user_controller(app):
    @app.action("user_info")
    def open_user_info(ack, body, client, logger):
        # 受信した旨を 3 秒以内に Slack サーバーに伝えます
        ack()
        user_id = body["user"]["id"]

        # ユーザー情報の取得
        user: Optional[User] = get_user(logger, user_id)

        # slackアカウントから名前（Display Name）Display Nameを取得する
        # display_nameを設定していない場合は、設定必須のreal_nameをユーザ名とすることで、対応する
        user_info = client.users_info(user=user_id)
        user_name = (
            user_info["user"]["profile"]["display_name"]
            or user_info["user"]["profile"]["real_name"]
        )

        modal_view = user_profile_modal(
            callback_id="user_profile_modal", user_name=user_name, user=user
        )

        client.views_open(
            trigger_id=body["trigger_id"],
            # ビューのペイロード
            view=modal_view,
        )

    # view_submission リクエストを処理
    @app.view("user_profile_modal")
    def handle_submission(ack, body, _, view, logger):

        user_name = view["blocks"][0]["text"]["text"]

        department = view["state"]["values"]["input_department"]["department_action"][
            "selected_option"
        ]["value"]

        job_type = view["state"]["values"]["input_job_type"]["job_type_action"][
            "selected_option"
        ]["value"]

        age_range = view["state"]["values"]["input_age_range"]["age_range_action"][
            "selected_option"
        ]["value"]

        user_id = body["user"]["id"]

        # view_submission リクエストの確認を行い、モーダルを閉じる
        ack()

        user: User = {
            "user_id": user_id,
            "user_name": user_name,
            "department": department,
            "job_type": job_type,
            "age_range": age_range,
            "updated_at": None,
        }

        add_user(logger, user)
