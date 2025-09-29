from datetime import datetime
from typing import List, Dict, Any
from model import Book
from pydantic import ValidationError
from typing import List, Dict
from model import Book
from pydantic import ValidationError

from datetime import datetime


def parse_book_line(line: str, line_number: int):
    parts = line.split("|")

    # support 3 atau 4 kolom
    if len(parts) == 3:
        title, author, publish_date = parts
    elif len(parts) == 4:
        _, title, author, publish_date = parts
    else:
        return {
            "line_number": line_number,
            "raw_data": line,
            "reason": "Invalid data structure (must be [id|]title|author|YYYY-MM-DD)",
        }

    try:
        payload = Book(
            book_title=title.strip(),
            author=author.strip(),
            publish_date=datetime.strptime(publish_date.strip(), "%Y-%m-%d"),
        )
        return payload
    except Exception:
        return {
            "line_number": line_number,
            "raw_data": line,
            "reason": "Invalid data types",
        }


def validate_books_payload(data: str) -> Dict:
    processed = 0
    issues = []
    valid_books: List[Book] = []

    for line_no, line in enumerate(data.splitlines(), start=1):
        parts = line.split("|")
        if len(parts) == 4:
            raw = {
                "id": parts[0],
                "book_title": parts[1],
                "author": parts[2],
                "publish_date": parts[3],
            }
            try:
                book = Book.model_validate(raw)
                valid_books.append(book)
                processed += 1
            except ValidationError as e:
                issues.append(
                    {
                        "line_number": line_no,
                        "raw_data": line,
                        "reason": str(e.errors()),
                    }
                )
        else:
            issues.append(
                {
                    "line_number": line_no,
                    "raw_data": line,
                    "reason": "Invalid data structure (expected 4 fields)",
                }
            )

    status = "Success" if processed > 0 else "Failed"
    return {
        "status": status,
        "processed_body_count": processed,
        "body_with_issues": len(issues),
        "issues": issues,
        "valid_books": valid_books,
    }


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
