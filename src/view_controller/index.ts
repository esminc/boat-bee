import { App } from "@slack/bolt";

import hello from "./hello";
import home from "./home";
import user from "./user";
import userList from "./userList";
import review from "./review";
import bookSearch from "./bookSearch";

function configure(app: App) {
  hello(app);
  home(app);
  user(app);
  userList(app);
  review(app);
  bookSearch(app);
}

export { configure };
