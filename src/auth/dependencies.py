from typing import List, Optional
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.auth.models import User
from .utils import decode_access_token
from src.db.redis import token_in_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import AuthService


auth_service = AuthService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        creds: HTTPAuthorizationCredentials = await super().__call__(request)

        if creds.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme",
            )

        if not self.token_is_valid(creds.credentials):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or has been revoked",
                    "resolution": "Please login again to get a new token",
                },
            )

        token_data = decode_access_token(creds.credentials)

        in_blocklist = await token_in_blocklist(token_data["jti"])

        if in_blocklist:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token has been revoked"
            )

        self.verify_token(token_data)

        return token_data

    def verify_token(self, token_data: dict) -> None:
        raise NotImplementedError("Subclasses must implement this method")

    def token_is_valid(self, token: str) -> bool:
        payload = decode_access_token(token)
        return payload is not None


class AcessTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict) -> None:

        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide access token",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict) -> None:

        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide refresh token",
            )


async def get_current_user(
    token_data: dict = Depends(AcessTokenBearer()),
    session: AsyncSession = Depends(get_session),
) -> dict:
    user_email = token_data["user"]["email"]

    user = await auth_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, user: User = Depends(get_current_user)) -> dict:
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "erorr": "Insufficient permissions",
                    "resolution": "Please contact an admin for access",
                },
            )

        return user
