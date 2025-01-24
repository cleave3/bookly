from src.db.models import User
from .schemas import UserCreateModel
from .utils import get_password_hash, verify_password
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class AuthService:

    # @staticmethod
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User | None:
        user = await session.exec(select(User).where(User.email == email))
        return user.first()

    # @staticmethod
    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return bool(user)

    async def create_user(
        self, user_data: UserCreateModel, session: AsyncSession
    ) -> User:
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password_hash = get_password_hash(user_data_dict["password"])
        new_user.role = "user"

        session.add(new_user)

        await session.commit()

        return new_user
