from fastapi import APIRouter, HTTPException, status
from typing import List
from .schemas import Book, BookUpdate
from .book_data import books

book_router = APIRouter()

@book_router.get('/', response_model=List[Book])
async def get_all_books():
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book:Book) -> dict:
    new_book = book.model_dump()

    books.append(new_book)

    return new_book

@book_router.patch('/{book_id}')
async def update_book(book_id: int, book_data: BookUpdate) -> dict:
   for book in books:
       if book["id"] == book_id:
        book["title"] = book_data.title
        book["page_count"] = book_data.page_count
        book["language"] = book_data.language
        return book
       
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.get('/{book_id}', status_code=status.HTTP_200_OK, response_model=Book)
async def get_book(book_id: int) -> dict:
   for book in books:
       if book["id"] == book_id:
           return book
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.delete('/{book_id}')
async def delete_book(book_id: int) -> dict:
   for book in books:
       if book["id"] == book_id:
           books.remove(book)
           return {"id": book_id, "message": "Book deleted successfully"}
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")