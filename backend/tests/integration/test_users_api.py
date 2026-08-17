import pytest
from uuid import UUID

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


