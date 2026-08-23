from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings

# ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword1")



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str: 
    to_encode = data.copy()
    issued_at = datetime.now(UTC)
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update(
        {
            "iat": issued_at,
            "exp": expire
        }
    )
    # to_encode["exp"] = expire # or if you had more fields to change, do to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.jwt_algorithm)
    return encoded_jwt


def create_jwt_refresh_token(data: dict[str, any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    issued_at = datetime.now(UTC)
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(days=settings.refresh_token_expire_days)
    )
    # jti is the JWT id
    to_encode.update(
        {
            "jti": str(uuid4()),
            "iat": issued_at,
            "exp": expire
        }
    )
    encoded_jwt = jwt.encode(to_encode, settings.secret_key.get_secret_value(), algorithm=settings.jwt_algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=[settings.jwt_algorithm])
