from slack_bolt import App

from bee_slack_app import ml
from bee_slack_app.service.review import post_review  # type: ignore
from bee_slack_app.view_controller import review

app = App(process_before_response=True)

review.review_controller(app)
