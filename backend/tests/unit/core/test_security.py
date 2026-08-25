from uuid import uuid4, UUID
import pytest

from datetime import timedelta
from jwt import InvalidTokenError

from app.core.security import (
    verify_password,
    get_password_hash,
    hash_refresh_token,
    create_access_token,
    create_jwt_refresh_token,
    decode_access_token,
    decode_refresh_token
)

def test_create_and_decode_access_token():
    user_id = uuid4()
    token = create_access_token(user_id)
    decoded_data = decode_access_token(token)
    assert UUID(decoded_data["sub"]) == user_id
    assert "exp" in decoded_data


def test_decode_expired_token_raises_error():
    token = create_access_token(uuid4(), expires_delta=timedelta(minutes=-1))
    with pytest.raises(InvalidTokenError):
        decode_access_token(token)

    rt = create_jwt_refresh_token(uuid4(), expires_delta=timedelta(minutes=-1))
    with pytest.raises(InvalidTokenError):
        decode_refresh_token(rt)


def test_decode_access_token_with_refresh():
    token = create_jwt_refresh_token(uuid4())
    with pytest.raises(InvalidTokenError):
        decode_access_token(token)


def test_decode_refresh_token_with_access():
    token = create_access_token(uuid4())
    with pytest.raises(InvalidTokenError):
        decode_refresh_token(token)



def test_create_and_decode_refresh_token():
    user_id = uuid4()
    refresh_token = create_jwt_refresh_token(user_id)
    decoded_data = decode_refresh_token(refresh_token.token)

    assert UUID(decoded_data["sub"]) == user_id
    assert "iat" in decoded_data
    assert "exp" in decoded_data
    assert "jti" in decoded_data


def test_password_hash_and_verify():
    plain = "my-password"
    hashed = get_password_hash(plain)

    assert hashed != plain
    assert verify_password(plain, hashed)
    assert not verify_password("wrong-password", hashed)


def test_hash_refresh_token():
    original_token = uuid4()
    hashed_token = hash_refresh_token(str(original_token))
    assert hashed_token != original_token

