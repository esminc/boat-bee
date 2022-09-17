/**
 * 本
 */
export type Book = {
  isbn: string;
  title: string;
  author: string;
  url: string;
  image_url: string;
  description: string;
  updated_at: string;
};

export type RecommendBook = Book & {
  interested: boolean;
  ml_model: string;
};

export type SearchedBook = {
  user_id: string;
  isbn: string;
  ml_model: string;
  interested: boolean;
  updated_at?: string;
};
