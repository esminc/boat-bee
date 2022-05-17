from typing import Optional

from bee_slack_app.model.user import User


def user_profile_modal(callback_id: str, user_name: str, user: Optional[User]):
    """
    ユーザプロフィールモーダル

    Args:
        callback_id: モーダルのcallback_id
        user_name: ユーザ名
        user: ユーザ
    """
    view = {
        "type": "modal",
        "callback_id": callback_id,
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
