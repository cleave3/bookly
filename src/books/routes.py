from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List
from .schemas import Book, BookCreateModel, BookUpdateModel
from .service import BookService
from src.db.main import get_session

book_router = APIRouter()
book_service = BookService()


@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)) -> List[dict]:
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(
    book: BookCreateModel, session: AsyncSession = Depends(get_session)
) -> dict:
    new_book = await book_service.create_book(book, session)
    return new_book


@book_router.patch("/{book_id}")
async def update_book(
    book_id: str,
    book_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:

    book = await book_service.update_book(book_id, book_data, session)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return book


@book_router.get("/{book_id}", status_code=status.HTTP_200_OK, response_model=Book)
async def get_book(book_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book_by_id(book_id, session)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return book


@book_router.delete("/{book_id}")
async def delete_book(
    book_id: int, session: AsyncSession = Depends(get_session)
) -> dict:
    book = await book_service.delete_book(book_id, session)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return {"message": "Book deleted successfully"}
