from datetime import timedelta
from uuid import UUID, uuid4
import pytest
from app.core.security import create_access_token, decode_access_token


@pytest.mark.asyncio
async def test_create_note(client, auth_token):
    response = await client.post(
        "api/v1/notes/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "title": "Test Note",
            "body": "Test Body"
        }
    )
    note = response.json()
    assert note["title"] == "Test Note"
    assert note["body"] == "Test Body"
    assert note["user_id"] == decode_access_token(auth_token)["sub"]


@pytest.mark.asyncio
async def test_update_note(client, auth_token):
    response = await client.post(
        "api/v1/notes/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "title": "Test Note",
            "body": "Test Body"
        }
    )
    note_id = UUID(response.json()["id"])

    response = await client.patch(
        f"api/v1/notes/{str(note_id)}",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "body": "Update body"
        }
    )

    note = response.json()
    assert UUID(note["id"]) == note_id
    assert note["title"] == "Test Note"
    assert note["body"] == "Update body"


# Authentication Error
@pytest.mark.asyncio
async def test_update_note_no_token(client, auth_token):
    response = await client.post(
        "api/v1/notes/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "title": "Test Note",
            "body": "Test Body"
        }
    )

    note_id = UUID(response.json()["id"])
    response = await client.patch(
            f"api/v1/notes/{str(note_id)}",
            json={
                "body": "Update body"
            }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


    response = await client.get(
        f"api/v1/notes/{str(note_id)}"
    )

    note = response.json()
    assert note["title"] == "Test Note"
    assert note["body"] == "Test Body"


# Authorization Error
@pytest.mark.asyncio
async def test_update_note_wrong_token(client, auth_token):
    response = await client.post(
        "api/v1/notes/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "title": "Test Note",
            "body": "Test Body"
        }
    )

    note_id = UUID(response.json()["id"])
    response = await client.patch(
            f"api/v1/notes/{str(note_id)}",
            headers={
                "Authorization": "Bearer wrong-token"
            },
            json={
                "body": "Update body"
            }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


    response = await client.get(
        f"api/v1/notes/{str(note_id)}"
    )

    note = response.json()
    assert note["title"] == "Test Note"
    assert note["body"] == "Test Body"


@pytest.mark.asyncio
async def test_update_note_expired_token(client, auth_token):
    response = await client.post(
        "api/v1/notes/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "title": "Test Note",
            "body": "Test Body"
        }
    )
    note_id = UUID(response.json()["id"])
    user_id = UUID(decode_access_token(auth_token)["sub"])
    good_token = create_access_token(data={"sub": str(user_id)})
    response = await client.patch(
            f"api/v1/notes/{str(note_id)}",
            headers={
                "Authorization": f"Bearer {good_token}"
            },
            json={
                "body": "Update body"
            }
    )

    assert response.json()["title"] == "Test Note"
    assert response.json()["body"] == "Update body"

    expired_token = create_access_token(data={"sub": str(user_id)}, expires_delta=timedelta(minutes=-1))
    response = await client.patch(
            f"api/v1/notes/{str(note_id)}",
            headers={
                "Authorization": f"Bearer {expired_token}"
            },
            json={
                "body": "Final Update"
            }
    )
    assert response.status_code == 401

    response = await client.get(
        f"api/v1/notes/{str(note_id)}"
    )

    assert response.json()["title"] == "Test Note"
    assert response.json()["body"] == "Update body"