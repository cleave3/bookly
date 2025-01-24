from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from src.books.schemas import Book


class UserModel(BaseModel):
    uid: uuid.UUID
    first_name: str
    last_name: str
    username: str
    email: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserBooks(UserModel):
    books: List[Book]


class UserCreateModel(BaseModel):
    first_name: str = Field(
        min_length=2,
        max_length=20,
        examples=["John"],
    )
    last_name: str = Field(min_length=2, max_length=20, examples=["Doe"])
    username: str = Field(max_length=8, examples=["johndoe"])
    email: str = Field(max_length=40, examples=["johndoe@mail.com"])
    password: str = Field(
        min_length=6,
        # pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$",
        description="Password must be at least 6 characters long and contain at least one uppercase letter, one lowercase letter, and one number.",
        title="Password",
        examples=["123456"],
    )


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40, examples=["johndoe@mail.com"])
    password: str = Field(
        min_length=6,
        # pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$",
        description="Password must be at least 6 characters long and contain at least one uppercase letter, one lowercase letter, and one number.",
        title="Password",
        examples=["123456"],
    )


# class LoginResponse(BaseModel):
#     access_token: str
#     refresh_token: str
#     user: dict[str, str]
