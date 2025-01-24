from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


class BooklyException(Exception):
    """This is the base class for all bookly errors"""

    pass


class InvalidToken(BooklyException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(BooklyException):
    """User has provided a token that has been revoked"""

    pass


class AccessTokenRequired(BooklyException):
    """User has provided a refresh token when an access token is needed"""

    pass


class RefreshTokenRequired(BooklyException):
    """User has provided an access token when a refresh token is needed"""

    pass


class UserAlreadyExists(BooklyException):
    """User has provided an email for a user who exists during sign up."""

    pass


class InvalidCredentials(BooklyException):
    """User has provided wrong email or password during log in."""

    pass


class InsufficientPermission(BooklyException):
    """User does not have the neccessary permissions to perform an action."""

    pass


class BookNotFound(BooklyException):
    """Book Not found"""

    pass


class UserNotFound(BooklyException):
    """User Not found"""

    pass


class AccountNotVerified(Exception):
    """Account not yet verified"""

    pass


class InternalServerError(Exception):
    """Internal Server Error"""

    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: BooklyException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "status": False,
                "code": status.HTTP_403_FORBIDDEN,
                "message": "User with email already exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "status": False,
                "code": status.HTTP_404_NOT_FOUND,
                "message": "User not found",
            },
        ),
    )
    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "status": False,
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Book not found",
            },
        ),
    )
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "status": False,
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid Email Or Password",
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "status": False,
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "Token is invalid Or expired",
            },
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "status": False,
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "Token is invalid or has been revoked",
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "status": False,
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "Please provide a valid access token",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "status": False,
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Please provide a valid refresh token",
            },
        ),
    )
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "status": False,
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "You do not have enough permissions to perform this action",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "status": False,
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Book Not Found",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "status": False,
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Account Not verified",
            },
        ),
    )

    # @app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    # async def internal_server_error(request, exc):

    #     return JSONResponse(
    #         content={
    #             "status": False,
    #             "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             "message": "Oops! Something went wrong",
    #
    #         },
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #     )

    # @app.exception_handler(SQLAlchemyError)
    # async def database__error(request, exc):
    #     print(str(exc))
    #     return JSONResponse(
    #         content={
    #             "status": False,
    #             "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             "message": "Oops! Something went wrong",
    #
    #         },
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #     )
