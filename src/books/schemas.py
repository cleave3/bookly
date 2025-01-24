from datetime import date, datetime

# from typing import Optional
from typing import Optional
import uuid
from pydantic import BaseModel


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime
    # user: Optional[User]


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
