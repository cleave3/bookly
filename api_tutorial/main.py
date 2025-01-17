from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello world"}

@app.get('/greet/{name}')
async def greet_name(name: str, age: int) -> dict:
    return {"message": f"Hello {name}", "age": age}

@app.get('/optional')
async def optional(age: int = 0, name: Optional[str] = "User") -> dict:
    return {"name": name, "age": age}


class BookCreateModel(BaseModel):
    title: str
    author: str

@app.post('/create-book')
async def create_book(book_data: BookCreateModel):
    return {
        "title": book_data.title,
        "author": book_data.author
    }

@app.get('/get-headers', status_code=200)
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None),
):
    request_headers = {
        "accept": accept,
        "content_type": content_type,
        "user_agent": user_agent,
        "host": host,
    }

    return request_headers