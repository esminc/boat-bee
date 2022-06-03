import json

from bee_slack_app.view.study_button import generate_test_button_model_view


def test_home_button_controller(app):  # pylint: disable=too-many-statements
    @app.action("test_home_button_action")
    def open_test_home_button_modal(ack, body, client):
        ack()

        # TODO: ボタン状態はDBから読み出す
        # とりあえず今は固定値で始める
        button_status_list = [False, False, False]

        modal_view = generate_test_button_model_view(
            # 興味なしボタンを表示
            callback_id="test_button_modal",
            button_status_list=button_status_list,
        )

        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )

    @app.action("test_button_switch_action")
    def handle_updete_button_action(ack, body, logger, client):

        ack()
        logger.info(body)

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
        modal_view = generate_test_button_model_view(
            callback_id="test_button_modal",
            button_status_list=button_status_list,
        )
        client.views_update(
            view_id=body["container"]["view_id"],
            view=modal_view,
        )

        # TODO: 最新のボタン状態をDBに格納する
