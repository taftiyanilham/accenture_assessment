from datetime import datetime
from typing import List, Dict, Any
from model import Book


def serialize_book(data):
    new_books: List[Any] = []
    for words in data.splitlines():
        splitted_words = words.split("|")
        if len(splitted_words) == 4:
            try:
                id = int(splitted_words[0])
            except ValueError:
                id = splitted_words[0]
            title = splitted_words[1]
            author = splitted_words[2]
            publication_date = splitted_words[3]
            book_data = {
                "id": id,
                "book_title": title,
                "author": author,
                "publish_date": datetime.strptime(publication_date, "%Y-%m-%d"),
            }
            try:
                Book(**book_data)
                new_books.append(book_data)
            except:
                continue
    return new_books


def serializer(data):
    processed_body_count = 0
    body_with_issue = 0
    issues = []
    books: List[Dict] = []

    for line, words in enumerate(data.splitlines()):
        splitted_words = words.split("|")
        if len(splitted_words) == 4:
            try:
                id = int(splitted_words[0])
            except ValueError:
                id = splitted_words[0]
            title = splitted_words[1]
            author = splitted_words[2]
            publication_date = splitted_words[3]
            book_data = {
                "id": id,
                "book_title": title,
                "author": author,
                "publish_date": datetime.strptime(publication_date, "%Y-%m-%d"),
            }
            try:
                Book(**book_data)
                processed_body_count += 1
                # books.append(data)
            except:
                body_with_issue += 1
                err = {
                    "line_number": line + 1,
                    "raw_data": words,
                    "reason": "Invalid data types",
                }
                issues.append(err)
        else:
            body_with_issue += 1
            err = {
                "line_number": line + 1,
                "raw_data": words,
                "reason": "Invalid data structures",
            }
            issues.append(err)
    status = "Success" if processed_body_count > 0 else "Failed"
    if books:
        serialize_book(books)
    result = {
        "status": status,
        "processed_body_count": processed_body_count,
        "body_with_issues": body_with_issue,
        "issues": issues,
    }
    return result
