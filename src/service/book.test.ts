import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { BookService } from "./book";

it("本を取得できること(全件取得の場合)", async () => {
  const target = new BookService();

  const books = await target.fetch({});

  expect(books?.items).toEqual([
    {
      isbn: "3456789012346",
      title: "dummy_title_2",
      author: "dummy_author_2",
      url: "dummy_url_2",
      imageUrl: "dummy_image_url_2",
      updatedAt: "2022-04-03T00:00:00+09:00",
    },
  ]);
});
