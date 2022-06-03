from bee_slack_app.view.test_button import generate_test_button_model_view


def test_home_button_controller(app):  # pylint: disable=too-many-statements
    @app.action("test_home_button_action")
    def open_test_home_button_modal(ack, body, client):
        ack()
        modal_view = generate_test_button_model_view(
            # 興味なしボタンを表示
            callback_id="test_button_modal",
            interested=False,
        )

        client.views_open(
            trigger_id=body["trigger_id"],
            view=modal_view,
        )

    @app.action("test_button_switch_action")
    def handle_some_action(ack, body, logger, client):
        print("body=", body)
        ack()
        logger.info(body)
        print("button_test_print")
        modal_view = generate_test_button_model_view(
            # 興味ありボタンを表示
            callback_id="test_button_modal",
            interested=True,
        )
        client.views_update(
            view_id=body["container"]["view_id"],
            view=modal_view,
        )
