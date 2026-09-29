from datetime import timedelta
from uuid import UUID

import pytest

from app.core.security import create_access_token, decode_access_token


@pytest.mark.asyncio
async def test_create_note(client, auth_token):
    response = await client.post(
        "api/v1/notes/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Test Note", "body": "Test Body"},
    )
    note = response.json()
    assert note["title"] == "Test Note"
    assert note["body"] == "Test Body"
    assert note["user_id"] == decode_access_token(auth_token)["sub"]


@pytest.mark.asyncio
async def test_update_note(client, auth_token):
    response = await client.post(
        "api/v1/notes/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Test Note", "body": "Test Body"},
    )
    note_id = UUID(response.json()["id"])

    response = await client.patch(
        f"api/v1/notes/{note_id!s}",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"body": "Update body"},
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
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Test Note", "body": "Test Body"},
    )

    note_id = UUID(response.json()["id"])
    response = await client.patch(f"api/v1/notes/{note_id!s}", json={"body": "Update body"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

    response = await client.get(f"api/v1/notes/{note_id!s}")

    note = response.json()
    assert note["title"] == "Test Note"
    assert note["body"] == "Test Body"


# Authorization Error
@pytest.mark.asyncio
async def test_update_note_wrong_token(client, auth_token):
    response = await client.post(
        "api/v1/notes/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Test Note", "body": "Test Body"},
    )

    note_id = UUID(response.json()["id"])
    response = await client.patch(
        f"api/v1/notes/{note_id!s}",
        headers={"Authorization": "Bearer wrong-token"},
        json={"body": "Update body"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

    response = await client.get(f"api/v1/notes/{note_id!s}")

    note = response.json()
    assert note["title"] == "Test Note"
    assert note["body"] == "Test Body"


@pytest.mark.asyncio
async def test_update_note_expired_token(client, auth_token):
    response = await client.post(
        "api/v1/notes/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Test Note", "body": "Test Body"},
    )
    note_id = UUID(response.json()["id"])
    user_id = UUID(decode_access_token(auth_token)["sub"])
    good_token = create_access_token(user_id)
    response = await client.patch(
        f"api/v1/notes/{note_id!s}",
        headers={"Authorization": f"Bearer {good_token}"},
        json={"body": "Update body"},
    )

    assert response.json()["title"] == "Test Note"
    assert response.json()["body"] == "Update body"

    expired_token = create_access_token(user_id, expires_delta=timedelta(minutes=-1))
    response = await client.patch(
        f"api/v1/notes/{note_id!s}",
        headers={"Authorization": f"Bearer {expired_token}"},
        json={"body": "Final Update"},
    )
    assert response.status_code == 401

    response = await client.get(f"api/v1/notes/{note_id!s}")

    assert response.json()["title"] == "Test Note"
    assert response.json()["body"] == "Update body"


@pytest.mark.asyncio
async def test_delete_note(client, auth_token):
    response = await client.post(
        "api/v1/notes/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Test Note", "body": "Test Body"},
    )
    note_id = UUID(response.json()["id"])

    response = await client.delete(
        f"api/v1/notes/{note_id!s}", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert UUID(response.json()["id"]) == note_id

    response = await client.get(f"api/v1/notes/{note_id!s}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_note_no_token(client, auth_token):
    response = await client.post(
        "api/v1/notes/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Test Note", "body": "Test Body"},
    )
    note_id = UUID(response.json()["id"])

    response = await client.delete(f"api/v1/notes/{note_id!s}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_note_wrong_owner(client, auth_token):
    response = await client.post(
        "api/v1/notes/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Test Note", "body": "Test Body"},
    )
    note_id = UUID(response.json()["id"])

    await client.post(
        "api/v1/auth/signup",
        json={"email": "other@test.com", "username": "OtherUser", "password": "123"},
    )
    other_login = await client.post(
        "api/v1/auth/token", data={"username": "OtherUser", "password": "123"}
    )
    other_token = other_login.json()["access_token"]

    response = await client.delete(
        f"api/v1/notes/{note_id!s}", headers={"Authorization": f"Bearer {other_token}"}
    )
    assert response.status_code == 403

    response = await client.get(f"api/v1/notes/{note_id!s}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_notes_filters_private_by_default(client, auth_token):
    await client.post(
        "api/v1/notes/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Private Note", "body": "Secret"},
    )
    await client.post(
        "api/v1/notes/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Public Note", "body": "Hello", "is_public": True},
    )

    response = await client.get("api/v1/notes/")
    assert response.status_code == 200
    titles = [n["title"] for n in response.json()]
    assert titles == ["Public Note"]


@pytest.mark.asyncio
async def test_get_notes_own_notes_include_private(client, auth_token):
    await client.post(
        "api/v1/notes/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Private Note", "body": "Secret"},
    )
    await client.post(
        "api/v1/notes/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Public Note", "body": "Hello", "is_public": True},
    )
    user_id = decode_access_token(auth_token)["sub"]

    response = await client.get(
        f"api/v1/notes/?user_id={user_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    titles = {n["title"] for n in response.json()}
    assert titles == {"Private Note", "Public Note"}


@pytest.mark.asyncio
async def test_get_notes_other_users_private_notes_hidden(client, auth_token):
    await client.post(
        "api/v1/notes/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "Private Note", "body": "Secret"},
    )
    user_id = decode_access_token(auth_token)["sub"]

    await client.post(
        "api/v1/auth/signup",
        json={"email": "other@test.com", "username": "OtherUser", "password": "123"},
    )
    other_login = await client.post(
        "api/v1/auth/token", data={"username": "OtherUser", "password": "123"}
    )
    other_token = other_login.json()["access_token"]

    response = await client.get(
        f"api/v1/notes/?user_id={user_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 200
    assert response.json() == []
