from slack_bolt import App

from bee_slack_app.view_controller import hello, review

app = App(process_before_response=True)

hello.hello_controller(app)
review.review_controller(app)
