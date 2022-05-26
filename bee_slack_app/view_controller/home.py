from logging import getLogger

from bee_slack_app.service.review import get_reviews
from bee_slack_app.service.user_action import record_user_action
from bee_slack_app.view.home import home


def home_controller(app):
    @app.event("app_home_opened")
    def update_home_view(ack, event, client):
        ack()

        reviews = get_reviews(logger=getLogger())

        total_review_count = len(reviews["items"]) if reviews else 0

        record_user_action(
            user_id=event["user"],
            action_type="app_home_opened",
            payload={"total_review_count": total_review_count},
        )

        client.views_publish(
            user_id=event["user"],
            view=home(
                read_review_action_id="read_review_action",
                post_review_action_id="post_review_action",
                see_more_recommended_book_action_id="book_recommend_action",
                user_info_action_id="user_info_action",
                total_review_count=total_review_count,
            ),
        )
