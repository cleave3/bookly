from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .models import Book
from .schemas import BookCreateModel, BookUpdateModel

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book_by_id(self, book_id: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_id)
        result = await session.exec(statement)
        book = result.first()

        return book if book else None

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)

        session.add(new_book)

        await session.commit()

        return new_book

    async def update_book(self, book_id: str, book_update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book_by_id(book_id, session)

        if not book_to_update:
            return None

        book_update_data = book_update_data.model_dump()

        for key, value in book_update_data.items():
            setattr(book_to_update, key, value)

        await session.commit()

        return book_to_update


    async def delete_book(self, book_id: str, session: AsyncSession):
        book_to_delete = await self.get_book_by_id(book_id, session)

        if not book_to_delete:
            return None

        session.delete(book_to_delete)

        session.commit()