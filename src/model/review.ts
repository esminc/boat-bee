export type Review = {
  user_id: string;
  book_title: string;
  isbn: string;
  score_for_me: string;
  score_for_others: string;
  review_comment: string;
  updated_at?: string;
  book_image_url: string;
  book_author: string;
  book_url: string;
  book_description: string;
  user_name?: string;
};
