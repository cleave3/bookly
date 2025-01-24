from datetime import date, datetime

# from typing import Optional
from typing import List, Optional
import uuid
from pydantic import BaseModel

from src.db.models import User


class BookReviewModel(BaseModel):
    rating: int
    comment: str
    created_at: datetime


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime


class BookDetailModel(Book):
    reviews: List[BookReviewModel]
    user: Optional[User]


class BookCreateModel(BaseModel):
    title: str
    author: str
    published_date: str
    page_count: int
    language: str
    published_date: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    published_date: str
    page_count: int
    language: str
