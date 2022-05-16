from bee_slack_app.view.book import see_more_recommended_book_modal


def book_controller(app):
    @app.action("see_more_recommended_book")
    def open_see_more_recommended_book_modal(ack, body, client):
        """
        あなたへのおすすめ本モーダル
        """
        ack()
        client.views_open(
            trigger_id=body["trigger_id"],
            view=see_more_recommended_book_modal(),
        )
