from typing import Optional

from bee_slack_app.model.user import User

# 表示内容と内部情報の対応を辞書形式で保持しておく
user_department_dict = {
    "its": "ITサービス事業部",
    "finance": "金融システム事業部",
    "medical": "医療システム事業部",
    "agile": "アジャイル事業部",
    "etec": "組み込み技術事業部",
    "medical-education": "医学教育支援室",
    "general": "管理部",
    "other": "その他",
}
user_job_type_dict = {
    "engineer": "開発・導入",
    "management": "マネジメント・営業",
    "executive": "経営",
    "other": "その他",
}
user_age_range_dict = {
    "10": "～19才",
    "20": "20才～29才",
    "30": "30才～39才",
    "40": "40才～49才",
    "50": "50才～59才",
    "60": "60才～",
}


def _make_options(source: dict[str, str]) -> list[dict]:
    """
    変換辞書の内容から画面表示用のOptionsを生成する
    """
    options = []
    for key, value in source.items():
        item = {
            "value": key,
            "text": {"type": "plain_text", "text": value},
        }

        options.append(item)
    return options


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
                    "action_id": "department_action",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "事業部を選択してください",
                        "emoji": True,
                    },
                    "options": _make_options(user_department_dict),
                },
            },
            {
                "type": "input",
                "block_id": "input_job_type",
                "label": {"type": "plain_text", "text": "主な仕事"},
                "element": {
                    "type": "static_select",
                    "action_id": "job_type_action",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "一番近いものを選択してください",
                        "emoji": True,
                    },
                    "options": _make_options(user_job_type_dict),
                },
            },
            {
                "type": "input",
                "block_id": "input_age_range",
                "label": {"type": "plain_text", "text": "年齢層"},
                "element": {
                    "type": "static_select",
                    "action_id": "age_range_action",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "年齢層を選択してください",
                        "emoji": True,
                    },
                    "options": _make_options(user_age_range_dict),
                },
            },
        ],
    }

    # ユーザー情報が登録されている場合に、そのユーザー情報を取得し表示する。
    if user:
        view["blocks"][1]["element"]["initial_option"] = {  # type: ignore
            "value": user["department"],
            "text": {
                "type": "plain_text",
                "text": user_department_dict[user["department"]],
            },
        }
        view["blocks"][2]["element"]["initial_option"] = {  # type: ignore
            "value": user["job_type"],
            "text": {
                "type": "plain_text",
                "text": user_job_type_dict[user["job_type"]],
            },
        }
        view["blocks"][3]["element"]["initial_option"] = {  # type: ignore
            "value": user["age_range"],
            "text": {
                "type": "plain_text",
                "text": user_age_range_dict[user["age_range"]],
            },
        }

    return view
