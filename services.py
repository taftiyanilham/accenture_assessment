# services.py
from sqlalchemy.orm import Session
from sql_models import BookDB
from model import Book
from datetime import datetime


class BookService:
    def __init__(self, db: Session):
        self.db = db

    def get_books_with_pagination(self, skip: int, limit: int):
        return self.db.query(BookDB).offset(skip).limit(limit).all()

    def get_book_by_title(self, title: str):
        """Cari buku berdasarkan judul"""
        return self.db.query(BookDB).filter(BookDB.book_title == title).first()

    def create_book(self, book_payload):
        book = BookDB(
            # id=book_payload.id,
            book_title=book_payload.book_title,
            author=book_payload.author,
            publish_date=book_payload.publish_date,
        )
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def create_books_from_text(self, text_data: str):
        new_books = []
        for line in text_data.splitlines():
            splitted = line.split("|")
            if len(splitted) == 4:
                try:
                    id = int(splitted[0])
                except ValueError:
                    continue
                title = splitted[1]
                author = splitted[2]
                try:
                    publish_date = datetime.strptime(splitted[3], "%Y-%m-%d").date()
                except ValueError:
                    continue

                book = BookDB(
                    id=id,
                    book_title=title,
                    author=author,
                    publish_date=publish_date,
                )
                self.db.add(book)
                new_books.append(book)
        self.db.commit()
        return new_books
