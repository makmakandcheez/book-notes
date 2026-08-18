import pytest
import pytest_asyncio
from uuid import UUID, uuid4

from app.core.security import decode_access_token

@pytest.mark.asyncio
async def test_read_users_me(client, auth_token):
    response = await client.get(
        "api/v1/users/me",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
    )

    assert response.status_code == 200
    user = response.json()
    assert user["id"] == decode_access_token(auth_token)["sub"]
    assert user["username"] == "Johnny" 


@pytest.mark.asyncio
async def test_get_user(client, auth_token):
    user_id = decode_access_token(auth_token)["sub"]
    response = await client.get(
        f"api/v1/users/{user_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["username"] == "Johnny" 



@pytest.mark.asyncio
async def test_get_user_wrong_id(client):
    wrong_id = uuid4()
    response = await client.get(
        f"api/v1/users/{wrong_id}"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
    

@pytest.mark.asyncio
async def test_delete_user(client, auth_token):
    user_id = decode_access_token(auth_token)["sub"]
    response = await client.delete(
        f"api/v1/users/{user_id}",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["username"] == "Johnny"

    response = await client.get(
        f"api/v1/users/{user_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_delete_user_forbidden(client, auth_token):
    user_id = uuid4()
    response = await client.delete(
        f"api/v1/users/{user_id}",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to delete this user"


@pytest.mark.asyncio
async def test_update_user(client, auth_token):
    user_id = decode_access_token(auth_token)["sub"]
    response = await client.patch(
        f"api/v1/users/{user_id}",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "username": "New Name"
        }
    )
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["username"] == "New Name"


@pytest_asyncio.fixture
async def post_10_users(client):
    for i in range(1, 11):
        await client.post(
            "api/v1/auth/signup",
            json={
                "username": f"user{i}",
                "email": f"{i}@test.com",
                "password": "123"
            }
        )

@pytest.mark.asyncio
async def test_get_users(client, post_10_users):
    response = await client.get(
        "api/v1/users/"
    )
  
    assert response.status_code == 200
    assert [user["username"] for user in response.json()] == [
        "user1", "user2", "user3", "user4", "user5"
    ]
    assert ("user6" or "user7" or "user8" or "user9" or "user10") not in [user["username"] for user in response.json()]


@pytest.mark.asyncio
async def test_get_users_pagination_params(client, post_10_users):
    response1 = await client.get("api/v1/users/?page=2")
    response2 = await client.get("api/v1/users/?limit=10")
    response3 = await client.get("api/v1/users/?page=2&limit=10")
    response4 = await client.get("api/v1/users/?page=3")
    response5 = await client.get("api/v1/users/?limit=11")
    response6 = await client.get("api/v1/users/?page=3&limit=2") # should be 5 and 6
    response7 = await client.get("api/v1/users/?limit=0")
    response8 = await client.get("api/v1/users/?limit=1&page=8") # return 8
    assert [user["username"] for user in response1.json()] == [
        "user6", "user7", "user8", "user9", "user10"
    ]
    assert [user["username"] for user in response2.json()] == [
        "user1", "user2", "user3", "user4", "user5",
        "user6", "user7", "user8", "user9", "user10"
    ]
    assert len(response3.json()) == 0
    assert len(response4.json()) == 0
    assert response5.status_code == 422
    assert [user["username"] for user in response6.json()] == [
        "user5", "user6"
    ]
    assert response7.status_code == 422
    assert [user["username"] for user in response8.json()] == [
        "user8"
    ]

@pytest.mark.asyncio
async def test_get_users_username_param(client, post_10_users):
    response = await client.get("api/v1/users/?username=user4")
    assert response.status_code == 200
    assert [user["username"] for user in response.json()] == ["user4"]


@pytest.mark.asyncio
async def test_get_users_username_param_no_user_found(client, post_10_users):
    response = await client.get("api/v1/users/?username=user11")
    assert response.status_code == 200
    assert response.json() == []