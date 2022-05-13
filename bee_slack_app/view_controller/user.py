from typing import Optional

from bee_slack_app.model.user import User
from bee_slack_app.service.user import add_user, get_user


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
        user_name = user_info["user"]["profile"]["display_name"] or user_info["user"]["profile"]["real_name"]

        modal_view = generate_user_input_modal_view(user_name, user)

        client.views_open(
            trigger_id=body["trigger_id"],
            # ビューのペイロード
            view=modal_view,
        )

    # view_submission リクエストを処理
    @app.view("view_user")
    def handle_submission(ack, body, _, view, logger):

        user_name = view["blocks"][0]["text"]["text"]

        department = view["state"]["values"]["input_department"][
            "action_id_department"
        ]["selected_option"]["value"]

        job_type = view["state"]["values"]["input_job_type"]["action_id_job_type"][
            "selected_option"
        ]["value"]

        age_range = view["state"]["values"]["input_age_range"]["action_id_age_range"][
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


def generate_user_input_modal_view(user_name: str, user: Optional[User]):
    view = {
        "type": "modal",
        # ビューの識別子
        "callback_id": "view_user",
        "title": {"type": "plain_text", "text": "プロフィール"},
        "submit": {"type": "plain_text", "text": "更新" if user else "登録", "emoji": True},
        "close": {"type": "plain_text", "text": "閉じる", "emoji": True},
        "blocks": [
            {
                "type": "section",
                "block_id": "section_user_name",
                "text": {
                    "type": "plain_text",
                    "text": user_name,
                },
            },
            {
                "type": "input",
                "block_id": "input_department",
                "label": {"type": "plain_text", "text": "事業部"},
                "element": {
                    "type": "static_select",
                    "action_id": "action_id_department",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "事業部を選択してください",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "value": "its",
                            "text": {"type": "plain_text", "text": "ITサービス事業部"},
                        },
                        {
                            "value": "finance",
                            "text": {"type": "plain_text", "text": "金融システム事業部"},
                        },
                        {
                            "value": "medical",
                            "text": {"type": "plain_text", "text": "医療システム事業部"},
                        },
                        {
                            "value": "agile",
                            "text": {
                                "type": "plain_text",
                                "text": "アジャイル事業部",
                            },
                        },
                        {
                            "value": "etec",
                            "text": {
                                "type": "plain_text",
                                "text": "組み込み技術事業部",
                            },
                        },
                        {
                            "value": "medical-education",
                            "text": {
                                "type": "plain_text",
                                "text": "医学教育支援室",
                            },
                        },
                        {
                            "value": "general",
                            "text": {"type": "plain_text", "text": "管理部"},
                        },
                        {
                            "value": "other",
                            "text": {"type": "plain_text", "text": "その他"},
                        },
                    ],
                },
            },
            {
                "type": "input",
                "block_id": "input_job_type",
                "label": {"type": "plain_text", "text": "主な仕事"},
                "element": {
                    "type": "static_select",
                    "action_id": "action_id_job_type",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "一番近いものを選択してください",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "value": "engineer",
                            "text": {"type": "plain_text", "text": "開発・導入"},
                        },
                        {
                            "value": "management",
                            "text": {"type": "plain_text", "text": "マネジメント・営業"},
                        },
                        {
                            "value": "executive",
                            "text": {"type": "plain_text", "text": "経営"},
                        },
                        {
                            "value": "other",
                            "text": {"type": "plain_text", "text": "その他"},
                        },
                    ],
                },
            },
            {
                "type": "input",
                "block_id": "input_age_range",
                "label": {"type": "plain_text", "text": "年齢層"},
                "element": {
                    "type": "static_select",
                    "action_id": "action_id_age_range",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "年齢層を選択してください",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "value": "10",
                            "text": {"type": "plain_text", "text": "～19才"},
                        },
                        {
                            "value": "20",
                            "text": {"type": "plain_text", "text": "20才～29才"},
                        },
                        {
                            "value": "30",
                            "text": {"type": "plain_text", "text": "30才～39才"},
                        },
                        {
                            "value": "40",
                            "text": {"type": "plain_text", "text": "40才～49才"},
                        },
                        {
                            "value": "50",
                            "text": {"type": "plain_text", "text": "50才～59才"},
                        },
                        {
                            "value": "60",
                            "text": {"type": "plain_text", "text": "60才～"},
                        },
                    ],
                },
            },
        ],
    }

    # ユーザー情報が登録されている場合に、そのユーザー情報を取得し表示する。
    if user:
        department_dict = {
            "its": "ITサービス事業部",
            "finance": "金融システム事業部",
            "medical": "医療システム事業部",
            "agile": "アジャイル事業部",
            "etec": "組み込み技術事業部",
            "medical-education": "医学教育支援室",
            "general": "管理部",
            "other": "その他",
        }
        view["blocks"][1]["element"]["initial_option"] = {  # type: ignore
            "value": user["department"],
            "text": {"type": "plain_text", "text": department_dict[user["department"]]},
        }

        job_type_dict = {
            "engineer": "開発・導入",
            "management": "マネジメント・営業",
            "executive": "経営",
            "other": "その他",
        }
        view["blocks"][2]["element"]["initial_option"] = {  # type: ignore
            "value": user["job_type"],
            "text": {"type": "plain_text", "text": job_type_dict[user["job_type"]]},
        }

        age_range_dict = {
            "10": "～19才",
            "20": "20才～29才",
            "30": "30才～39才",
            "40": "40才～49才",
            "50": "50才～59才",
            "60": "60才～",
        }
        view["blocks"][3]["element"]["initial_option"] = {  # type: ignore
            "value": user["age_range"],
            "text": {"type": "plain_text", "text": age_range_dict[user["age_range"]]},
        }

    return view
