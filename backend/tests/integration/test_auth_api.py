import pytest

from app.core.security import decode_access_token

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "api/v1/auth/signup",
        json={
            "email": "test@example.com",
            "username": "Johnny",
            "password": "123"
            }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "Johnny" 


@pytest.mark.asyncio
async def test_login_for_access_token(client):
    await client.post(
        "api/v1/auth/signup",
        json={
            "email": "test@example.com",
            "username": "Johnny",
            "password": "123"
            }
    )
    response = await client.post(
        "api/v1/auth/token",
        data={"username": "Johnny",
              "password": "123"
              }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    decoded_token = decode_access_token(token)
    assert int(decoded_token["sub"]) == 1
    assert "exp" in decoded_token


