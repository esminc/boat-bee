export type Review = {
  userId: string;
  bookTitle: string;
  isbn: string;
  scoreForMe: string;
  scoreForOthers: string;
  reviewComment: string;
  updatedAt?: string;
  bookImageUrl: string;
  bookAuthor: string;
  bookUrl: string;
  bookDescription: string;
  userName?: string;
};
