from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

from src.db.models import Book
from .schemas import BookCreateModel, BookUpdateModel
from datetime import datetime


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_user_book_submission(self, user_uid: str, session: AsyncSession):
        result = await session.exec(
            select(Book)
            .where(Book.user_uid == user_uid)
            .order_by(desc(Book.created_at))
        )
        return result.all()

    async def get_book_by_id(self, book_id: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_id)
        result = await session.exec(statement)
        book = result.first()

        if not book:
            return None

        return book

    async def create_book(
        self, book_data: BookCreateModel, user_uid: str, session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)

        new_book.published_date = datetime.strptime(
            book_data_dict["published_date"], "%Y-%m-%d"
        )

        new_book.user_uid = user_uid

        session.add(new_book)

        await session.commit()

        await session.refresh(new_book)

        return new_book

    async def update_book(
        self, book_id: str, book_update_data: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_book_by_id(book_id, session)

        if not book_to_update:
            return None

        book_update_data = book_update_data.model_dump()

        for key, value in book_update_data.items():
            # if key == "published_date":
            #     value = datetime.strptime(value, "%Y-%m-%d")
            setattr(book_to_update, key, value)

        await session.commit()

        return book_to_update

    async def delete_book(self, book_id: str, session: AsyncSession):
        book_to_delete = await self.get_book_by_id(book_id, session)

        if not book_to_delete:
            return None

        session.delete(book_to_delete)

        await session.commit()

        return book_to_delete
