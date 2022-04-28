from slack_bolt import App

from bee_slack_app.view_controller import book, book_search, hello, home, review, user

app = App(process_before_response=True)

hello.hello_controller(app)
review.review_controller(app)
home.home_controller(app)
book_search.book_search_controller(app)
book.book_controller(app)
user.user_controller(app)
