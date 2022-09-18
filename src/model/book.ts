/**
 * 本
 */
export type Book = {
  isbn: string;
  title: string;
  author: string;
  url: string;
  imageUrl: string;
  description: string;
  updatedAt: string;
};

export type RecommendBook = Book & {
  interested: boolean;
  mlModel: string;
};

export type SearchedBook = {
  userId: string;
  isbn: string;
  mlModel: string;
  interested: boolean;
  updatedAt?: string;
};
