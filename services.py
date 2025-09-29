from datetime import datetime
from typing import List, Dict, Any

books_dummy = [
    {
        "id": 1,
        "book_title": "It Depends",
        "author": "the practical dev",
        "publish_date": datetime(2021, 3, 25).date(),
    },
    {
        "id": 2,
        "book_title": "Python Programming",
        "author": "guido von rossum",
        "publish_date": datetime(1991, 2, 12).date(),
    },
]


class BookService:
    def get_default_books_with_pagination(self, skip: int, limit: int):
        if limit == 0:
            return books_dummy[skip:]
        return books_dummy[skip : skip + limit]

    def get_books_with_pagination(self, skip: int, limit: int, books: List[Any]):
        if limit == 0:
            return books[skip:]
        return books[skip : skip + limit]
