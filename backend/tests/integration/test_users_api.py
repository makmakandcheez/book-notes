import pytest


@pytest.mark.asyncio
async def test_read_users_me(client):
    await client.post(
        "api/v1/auth/signup",
        json={
            "email": "test@test.com",
            "username": "tester",
            "password": "1234"
        })

    response = await client.post(
        "api/v1/auth/token",
        data={
            "username": "tester",
            "password": "1234"
        }
    )

    token = response.json()["access_token"]
    print(token)
    response = await client.get(
        "api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200
    user = response.json()
    assert int(user["usr_id"]) == 1
    assert user["usr_username"] == "tester" 
