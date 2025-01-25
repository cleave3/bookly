import logging
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from src.config import Config
import uuid
from itsdangerous import URLSafeTimedSerializer

pwd_context = CryptContext(schemes=["bcrypt"])
serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET, salt="email-configuration"
)

ACCESS_TOKEN_EXPIRY = 1
REFRESH_TOKEN_EXPIRY = 2


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, refresh: bool = False) -> str:
    token = jwt.encode(
        payload={
            "exp": (
                datetime.now()
                + timedelta(
                    days=REFRESH_TOKEN_EXPIRY if refresh else ACCESS_TOKEN_EXPIRY
                )
            ),
            "user": data,
            "jti": str(uuid.uuid4()),
            "refresh": refresh,
        },
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )

    return token


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


def create_url_safe_token(data: dict):

    token = serializer.dumps(data)

    return token


def decode_url_safe_token(token: str) -> dict:
    try:
        token_data = serializer.loads(token)
        return token_data
    except Exception as e:
        logging.error(e)
        return None
