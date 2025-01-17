from fastapi import FastAPI
from src.books.routes import book_router

version = "v1"

app = FastAPI(
 version=version,
 title="Book Service",
 description="A book management portal"
)

app.include_router(book_router, tags=["Books"], prefix=f"/api/{version}/books")