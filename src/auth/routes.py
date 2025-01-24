from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.db.redis import add_jti_to_block_list
from .schemas import UserCreateModel, UserModel, UserLoginModel, UserBooks
from .service import AuthService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import create_access_token, verify_password
from .dependencies import RefreshTokenBearer, AcessTokenBearer, get_current_user
import datetime


auth_router = APIRouter()
user_service = AuthService()


@auth_router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=UserModel
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists.",
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    password = user_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid login credentials",
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid login credentials",
        )

    access_token = create_access_token(
        data={"email": email, "uid": str(user.uid), "role": user.role}
    )

    refresh_token = create_access_token(
        data={"email": email, "uid": str(user.uid), "role": user.role}, refresh=True
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "uid": str(user.uid),
                "email": email,
            },
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.get("/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_token(
    token_data: dict = Depends(RefreshTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    if datetime.fromtimestamp(token_data["exp"]) > datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token expired"
        )

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )

    user = await user_service.get_user_by_email(token_data["user"]["email"], session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token"
        )

    access_token = create_access_token(data=token_data["user"], refresh=False)

    return JSONResponse(
        content={"access_token": access_token},
        status_code=status.HTTP_200_OK,
    )


@auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserBooks)
async def get_current_user(user: dict = Depends(get_current_user)):

    return user


@auth_router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(token_data: dict = Depends(AcessTokenBearer())):
    await add_jti_to_block_list(token_data["jti"])

    return JSONResponse(
        content={"message": "Logout successful"},
        status_code=status.HTTP_200_OK,
    )
