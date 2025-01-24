from src.auth.service import AuthService
from src.db.models import Review
from src.books.service import BookService
from src.errors import BookNotFound, InternalServerError
from src.reviews.schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
import logging


book_service = BookService()
user_service = AuthService()


class ReviewService:

    async def submit_review(
        self,
        user_uid: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ) -> Review:

        try:

            book = await book_service.get_book_by_id(book_uid, session)

            if not book:
                raise BookNotFound()

            # user = await user_service.get_user_by_id(user_uid, session)

            new_review = Review(
                **review_data.model_dump(),
                book_uid=book_uid,
                user_uid=user_uid,
                # user=user,
                # book=book,
            )

            session.add(new_review)
            await session.commit()

            return new_review
        except Exception as e:
            logging.error(e)
            await session.rollback()
            raise InternalServerError()
