from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List
from .schemas import Book, BookCreateModel, BookDetailModel, BookUpdateModel
from .service import BookService
from src.db.main import get_session
from src.auth.dependencies import AcessTokenBearer, RoleChecker
from src.errors import BookNotFound

book_router = APIRouter()
book_service = BookService()
auth_user = Depends(AcessTokenBearer())
role_checker = Depends(RoleChecker(["user"]))


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    dependencies=[role_checker],
)
async def create_book(
    book: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    auth_user: dict = auth_user,
) -> dict:
    user_uid = auth_user.get("user")["uid"]
    new_book = await book_service.create_book(book, user_uid, session)
    return new_book


@book_router.patch(
    "/{book_id}", response_model=Book, dependencies=[role_checker, auth_user]
)
async def update_book(
    book_id: str,
    book_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:

    book = await book_service.update_book(book_id, book_data, session)

    if not book:
        raise BookNotFound()

    return book


@book_router.get("/", response_model=List[Book], dependencies=[role_checker, auth_user])
async def get_all_books(session: AsyncSession = Depends(get_session)) -> List[dict]:
    books = await book_service.get_all_books(session)
    return books


@book_router.get("/user", response_model=List[Book], dependencies=[role_checker])
async def get_user_book_submissions(
    session: AsyncSession = Depends(get_session), auth=auth_user
) -> List[dict]:
    books = await book_service.get_user_book_submission(
        auth.get("user")["uid"], session
    )
    return books


@book_router.get(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=BookDetailModel,
    dependencies=[role_checker, auth_user],
)
async def get_book(book_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book_by_id(book_id, session)

    if not book:
        raise BookNotFound()

    return book


@book_router.delete("/{book_id}", dependencies=[role_checker, auth_user])
async def delete_book(
    book_id: str, session: AsyncSession = Depends(get_session)
) -> dict:
    book = await book_service.delete_book(book_id, session)

    if not book:
        raise BookNotFound()

    return {"message": "Book deleted successfully"}
