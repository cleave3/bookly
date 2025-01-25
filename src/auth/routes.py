from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from src.db.redis import add_jti_to_block_list
from .schemas import (
    EmailModel,
    PasswordResetConfirmModel,
    PasswordResetRequestModel,
    SignUpResponseModel,
    UserCreateModel,
    UserLoginModel,
    UserBooks,
)
from .service import AuthService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import (
    create_access_token,
    verify_password,
    create_url_safe_token,
    decode_url_safe_token,
    get_password_hash,
)
from .dependencies import RefreshTokenBearer, AcessTokenBearer, get_current_user
from src.errors import InvalidCredentials, UserAlreadyExists, InvalidToken, UserNotFound
from src.config import Config

# from src.mail import mail, create_message
from src.celery_tasks import send_email


auth_router = APIRouter()
user_service = AuthService()


@auth_router.post("/send-email")
async def send_email(emails: EmailModel):
    try:
        # recipients = emails.addresses

        # html = """
        #     <h1>Welcome to Bookly</h1>
        # """

        # send_email.delay(recipients=recipients, subject="Welcome", body=html)
        # message = create_message(recipients=recipients, subject="Welcome", body=html)

        # await mail.send_message(message=message)

        return {"message": "Email sent successfully"}
    except Exception as e:
        print(e)
        {"message": e}
        # raise InternalServerError()


@auth_router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=SignUpResponseModel
)
async def create_user_account(
    user_data: UserCreateModel,
    bg_task: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    # link = f"{Config.BASE_URL}/api/v1/auth/verify/{create_url_safe_token({"email": email})}"

    # html = f"""
    #     <h1>Verify your Email</h1>
    #     <p>Please click <a href="{link}">here</a> to verify your email</p>
    # """

    # send_email.delay(recipients=[email], subject="Welcome", body=html)
    # message = create_message(recipients=[email], subject="Verify Your Email", body=html_msg)

    # # print(html_msg)

    # bg_task.add_task(mail.send_message, html_msg)

    return {
        "message": "Signup successful, Please check your email to verify your account",
        "user": new_user,
    }


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    password = user_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is None:
        raise InvalidCredentials()

    if not verify_password(password, user.password_hash):
        raise InvalidCredentials()

    # if not user.is_verified:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Please verify your email to proceed",
    #     )

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


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if not user_email:
        raise UserNotFound()

    user = await user_service.get_user_by_email(email=user_email, session=session)

    if not user:
        raise UserNotFound()

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="user already verified"
        )

    await user_service.update_user(
        user=user, user_data={"is_verified": True}, session=session
    )

    return JSONResponse(
        content={"message": "Account verified sucessfully"},
        status_code=status.HTTP_200_OK,
    )


@auth_router.get("/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_token(
    token_data: dict = Depends(RefreshTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    # if datetime.fromtimestamp(token_data["exp"]) > datetime.now():
    #     raise InvalidToken()

    if token_data is None:
        raise InvalidToken()

    user = await user_service.get_user_by_email(token_data["user"]["email"], session)

    if user is None:
        raise InvalidToken()

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


@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel):
    email = email_data.email

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
    <h1>Reset Your Password</h1>
    <p>Please click this <a href="{link}">link</a> to Reset Your Password</p>
    """
    subject = "Reset Your Password"

    send_email.delay([email], subject, html_message)
    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password",
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    new_password = passwords.new_password
    confirm_password = passwords.confirm_new_password

    if new_password != confirm_password:
        raise HTTPException(
            detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
        )

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        passwd_hash = get_password_hash(new_password)
        await user_service.update_user(user, {"password_hash": passwd_hash}, session)

        return JSONResponse(
            content={"message": "Password reset Successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during password reset."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
