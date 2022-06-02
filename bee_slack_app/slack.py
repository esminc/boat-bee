from slack_bolt import App

from bee_slack_app.view_controller import (
    book_search,
    hello,
    home,
    recommend,
    review,
    test_home_button,
    user,
)

app = App(process_before_response=True)

hello.hello_controller(app)
review.review_controller(app)
home.home_controller(app)
book_search.book_search_controller(app)
user.user_controller(app)
recommend.recommend_controller(app)
test_home_button.test_home_button_controller(app)
