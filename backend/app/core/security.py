import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings

# ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword1")

@dataclass
class RefreshTokenData:
    jti: UUID
    user_id: UUID
    token: str
    expires_at: datetime

@dataclass
class TokenPair:
    access_token: str
    refresh_token: str



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_access_token(user_id: UUID, expires_delta: timedelta | None = None) -> str:
    jti = uuid4()
    issued_at = datetime.now(UTC)
    expire = issued_at + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode = {
            "sub": str(user_id),
            "jti": str(jti),
            "iat": issued_at,
            "exp": expire,
            "type": "access"
        }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def create_jwt_refresh_token(
        user_id: UUID,
        expires_delta: timedelta | None = None
    ) -> RefreshTokenData:
    jti = uuid4()
    issued_at = datetime.now(UTC)
    expire = issued_at + (
        expires_delta or timedelta(days=settings.refresh_token_expire_days)
    )
    # jti is the JWT id
    to_encode = {
            "sub": str(user_id),
            "jti": str(jti),
            "iat": issued_at,
            "exp": expire,
            "type": "refresh"
        }
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm
    )
    return RefreshTokenData(
        user_id=user_id,
        token=encoded_jwt,
        jti=jti,
        expires_at=expire
    )


def decode_access_token(token: str) -> dict[str, Any]:
    data = jwt.decode(
        token,
        settings.secret_key.get_secret_value(),
        algorithms=[settings.jwt_algorithm],
        options=jwt.types.Options(
            require=["sub", "jti", "type", "exp", "iat"]
        )
    )
    if data["type"] != "access":
        raise InvalidTokenError
    return data


def decode_refresh_token(token: str)-> dict[str, Any]:
    # reference: https://pyjwt.readthedocs.io/en/latest/api.html#jwt.decode
    data = jwt.decode(
        token,
        settings.secret_key.get_secret_value(),
        algorithms=[settings.jwt_algorithm],
        options=jwt.types.Options(
            require=["sub", "jti", "type", "exp", "iat"]
        )
    )
    if data["type"] != "refresh":
        raise InvalidTokenError
    return data
