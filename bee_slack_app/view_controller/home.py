from logging import getLogger

from bee_slack_app.service.review import get_reviews
from bee_slack_app.view.home import home


def home_controller(app):
    @app.event("app_home_opened")
    def update_home_view(ack, event, client):
        ack()

        reviews = get_reviews(logger=getLogger(), limit=None, keys=[])

        if reviews is None:
            review_count_all = 0
        else:
            review_count_all = len(reviews["items"])

        client.views_publish(
            user_id=event["user"],
            view=home(
                read_review_action_id="read_review",
                post_review_action_id="post_review",
                see_more_recommended_book_action_id="book_recommend",
                user_info_action_id="user_info",
                review_count_all=review_count_all,
            ),
        )
