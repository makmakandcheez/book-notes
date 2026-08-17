from datetime import timedelta

import pytest
from app.core.security import create_access_token


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
    assert int(note["id"]) == 1
    assert note["title"] == "Test Note"
    assert note["body"] == "Test Body"
    assert note["user_id"] == 1


@pytest.mark.asyncio
async def test_update_note(client, auth_token):
    await client.post(
        "api/v1/notes/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "title": "Test Note",
            "body": "Test Body"
        }
    )

    response = await client.patch(
        "api/v1/notes/1",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "body": "Update body"
        }
    )

    note = response.json()
    assert note["title"] == "Test Note"
    assert note["body"] == "Update body"


# Authentication Error
@pytest.mark.asyncio
async def test_update_note_no_token(client, auth_token):
    await client.post(
        "api/v1/notes/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "title": "Test Note",
            "body": "Test Body"
        }
    )

    response = await client.patch(
            "api/v1/notes/1",
            json={
                "body": "Update body"
            }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


    response = await client.get(
        "api/v1/notes/1"
    )

    note = response.json()
    assert note["title"] == "Test Note"
    assert note["body"] == "Test Body"


# Authorization Error
@pytest.mark.asyncio
async def test_update_note_wrong_token(client, auth_token):
    await client.post(
        "api/v1/notes/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "title": "Test Note",
            "body": "Test Body"
        }
    )

    response = await client.patch(
            "api/v1/notes/1",
            headers={
                "Authorization": "Bearer wrong-token"
            },
            json={
                "body": "Update body"
            }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Coud not validate credentials"


    response = await client.get(
        "api/v1/notes/1"
    )

    note = response.json()
    assert note["title"] == "Test Note"
    assert note["body"] == "Test Body"


@pytest.mark.asyncio
async def test_update_note_expired_token(client, auth_token):
    await client.post(
        "api/v1/notes/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "title": "Test Note",
            "body": "Test Body"
        }
    )

    good_token = create_access_token(data={"sub": "1"})
    response = await client.patch(
            "api/v1/notes/1",
            headers={
                "Authorization": f"Bearer {good_token}"
            },
            json={
                "body": "Update body"
            }
    )

    assert response.json()["title"] == "Test Note"
    assert response.json()["body"] == "Update body"

    expired_token = create_access_token(data={"sub": "1"}, expires_delta=timedelta(minutes=-1))
    response = await client.patch(
            "api/v1/notes/1",
            headers={
                "Authorization": f"Bearer {expired_token}"
            },
            json={
                "body": "Final Update"
            }
    )
    assert response.status_code == 401

    response = await client.get(
        "api/v1/notes/1"
    )

    assert response.json()["title"] == "Test Note"
    assert response.json()["body"] == "Update body"