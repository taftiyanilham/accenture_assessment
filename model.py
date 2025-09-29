from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
from datetime import date


class Book(BaseModel):
    # id: int = Field(..., gt=0, description="Book ID must be positive integer")
    book_title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    publish_date: date

    class Config:
        from_attributes = True


class BodyError(BaseModel):
    line_number: int
    raw_data: str
    reason: str


class FileProcessResponse(BaseModel):
    status: str
    processed_body_count: int
    body_with_issues: int
    issues: List[BodyError] = []


class FileProcessErrorResponse(FileProcessResponse):
    reason: Optional[str]


class PaginatedBooksResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[Book]
