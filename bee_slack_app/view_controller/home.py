from bee_slack_app.view.home import home


def home_controller(app):
    @app.event("app_home_opened")
    def update_home_view(ack, event, client):
        ack()

        client.views_publish(
            user_id=event["user"],
            view=home(
                read_review_action_id="read_review",
                post_review_action_id="post_review",
                see_more_recommended_book_action_id="book_recommend",
                user_info_action_id="user_info",
            ),
        )
