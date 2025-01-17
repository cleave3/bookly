from typing import Optional
from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author:str
    published_date:str
    page_count: int
    language:str

class BookUpdate(BaseModel):
    title: Optional[str]
    page_count: Optional[int]
    language:Optional[str]