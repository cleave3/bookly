from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field


class Review(BaseModel):
    uid: uuid.UUID
    rating: int
    comment: str
    book_uid: Optional[uuid.UUID]
    user_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel(BaseModel):
    rating: int = Field(
        ge=1,
        le=5,
        examples=[5],
        description="Rating must be an integer between 1 and 5",
    )
    comment: str = Field(examples=["A good read"])
