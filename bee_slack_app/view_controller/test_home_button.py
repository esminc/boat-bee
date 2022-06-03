import json
from bee_slack_app.view.test_button import generate_test_button_model_view


def test_home_button_controller(app):  # pylint: disable=too-many-statements
    @app.action("test_home_button_action")
    def open_test_home_button_modal(ack, body, client):
        ack()
        modal_view = generate_test_button_model_view(
            # 興味なしボタンを表示
            callback_id="test_button_modal",
            interested=[False, False, False],
        )

        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )

    @app.action("test_button_switch_action")
    def handle_updete_button_action(ack, body, logger, client):
        private_metadata = body["view"]["private_metadata"]
        # private_metadataに格納していた情報を復元する
        interested_dict = json.loads(private_metadata)
        interested_list = interested_dict["interested"]
        value_data = int(body["actions"][0]["value"])

        # 押されたボタンを反転させる
        interested_list[value_data] = not interested_list[value_data]

        ack()
        logger.info(body)
        modal_view = generate_test_button_model_view(
            # 興味ありボタンの表示を切り替える
            callback_id="test_button_modal",
            interested=interested_list,
        )
        client.views_update(
            view_id=body["container"]["view_id"],
            view=modal_view,
        )
