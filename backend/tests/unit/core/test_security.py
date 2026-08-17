from uuid import uuid4, UUID

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)

def test_create_and_decode_access_token():
    user_id = uuid4()
    data = {"sub": str(user_id)}
    token = create_access_token(data)
    decoded_data = decode_access_token(token)
    assert UUID(decoded_data["sub"]) == user_id
    assert "exp" in decoded_data


def test_create_and_decode_access_token_with_role():
    user_id = uuid4()
    data = {
        "sub": str(user_id),
        "role": "user",
        }
    
    token = create_access_token(data)
    decoded_data = decode_access_token(token)

    assert UUID(decoded_data["sub"]) == user_id
    assert decoded_data["role"] == "user"
    assert "exp" in decoded_data


def test_password_hash_and_verify():
    plain = "my-password"
    hashed = get_password_hash(plain)

    assert hashed != plain
    assert verify_password(plain, hashed)
    assert not verify_password("wrong-password", hashed)



