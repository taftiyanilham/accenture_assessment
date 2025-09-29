from datetime import datetime
from model import Book


def parse_book_line(line: str, line_number: int):
    parts = line.split("|")

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
