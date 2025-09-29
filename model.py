from typing import List
from pydantic import BaseModel
from datetime import date


class Book(BaseModel):
    id: int
    book_title: str
    author: str
    publish_date: date


class BodyError(BaseModel):
    line_number: int
    raw_data: str
    reason: str


class FileProcessResponse(BaseModel):
    status: str
    processed_body_count: int
    body_with_issues: int
    issues: List[BodyError]


class FileProcessErrorResponse(FileProcessResponse):
    reason: str


class PaginatedBooksResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[Book]
