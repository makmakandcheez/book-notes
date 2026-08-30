from uuid import UUID

import pytest

from app.core.security import decode_access_token, decode_refresh_token


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
    response = await client.post(
        "api/v1/auth/signup",
        json={
            "email": "test@example.com",
            "username": "Johnny",
            "password": "123"
            }
    )
    user_id = UUID(response.json()["id"])
    response = await client.post(
        "api/v1/auth/token",
        data={"username": "Johnny", "password": "123"}
    )
    assert response.status_code == 200
    access_token = decode_access_token(response.json()["access_token"])
    assert access_token["sub"] == str(user_id)
    assert "exp" in access_token
    refresh_token = decode_refresh_token(response.json()["refresh_token"])
    assert refresh_token["sub"] == str(user_id)
    assert "jti" in refresh_token
    assert "iat" in refresh_token
    assert "exp" in refresh_token


@pytest.mark.asyncio
async def test_refresh(client):
    await client.post(
        "api/v1/auth/signup",
        json={
            "email": "test@test.com",
            "username": "Tester",
            "password": "123"
        }
    )
    login_response = await client.post(
        "api/v1/auth/token",
        data={"username": "Tester", "password": "123"}
    )
    access = login_response.json()["access_token"]
    rt = login_response.json()["refresh_token"]

    refresh_response = await client.post(
        "api/v1/auth/refresh-token",
        json={
            "refresh_token": str(rt)
        }
    )
    assert refresh_response.status_code == 200
    new_access = refresh_response.json()["access_token"]
    new_rt = refresh_response.json()["refresh_token"]

    assert new_access != access
    assert new_rt != rt
    # more thngs to assert



