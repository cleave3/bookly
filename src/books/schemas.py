from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author:str
    published_date:str
    page_count: int
    language:str
    created_at: datetime
    updated_at: datetime

class BookCreateModel(BaseModel):
    title: str
    author:str
    published_date:str
    page_count: int
    language:str
    published_date: str

class BookUpdateModel(BaseModel):
    title: str
    author:str
    published_date:str
    page_count: int
    language:str