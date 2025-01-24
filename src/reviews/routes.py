from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import AcessTokenBearer
from src.db.main import get_session
from src.db.models import Review
from src.errors import InternalServerError
from src.reviews.schemas import ReviewCreateModel
from src.reviews.service import ReviewService

reviews_router = APIRouter()

review_service = ReviewService()
auth_user = Depends(AcessTokenBearer())


@reviews_router.post("/book/{book_id}", response_model=Review)
async def submit_review(
    book_id: str,
    review_data: ReviewCreateModel,
    auth: dict = auth_user,
    session: AsyncSession = Depends(get_session),
):
    try:
        review = await review_service.submit_review(
            user_uid=auth.get("user")["uid"],
            book_uid=book_id,
            review_data=review_data,
            session=session,
        )
        return review
    except Exception as e:
        raise InternalServerError()
