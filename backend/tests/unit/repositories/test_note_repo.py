from uuid import uuid4

import pytest

from app.models.note import Note
from app.models.user import User


@pytest.mark.asyncio
async def test_create_note(note_repo):
    userid=uuid4()
    note=await note_repo.create_note(
        Note(
            title="Title",
            body="Body",
            is_public=True,
            user_id=userid
            )
        )
    assert note.user_id==userid
    assert note.title=="Title"
    assert note.is_public


@pytest.mark.asyncio
async def test_filter_notes(note_repo,user_repo):
    user=await user_repo.create_user(
        User(
            username="John",
            email="test@test.com",
            hashed_password="123"
            )
        )
    note=await note_repo.create_note(
        Note(
            title="Title",
            body="Body",
            user_id=user.id,
            is_public=True
            )
        )
    assert note.user_id==user.id
    result=await note_repo.filter_note(user_id=user.id, is_public=True)
    print(result)
    assert len(result) ==1
    assert result[0].title == "Title"


@pytest.mark.asyncio
async def test_get_notes(note_repo,user_repo):
    user=await user_repo.create_user(
        User(
            username="John",
            email="test@test.com",
            hashed_password="123"
            )
        )
    note=await note_repo.create_note(
        Note(
            title="Title",
            body="Body",
            user_id=user.id
            )
        )
    assert note.user_id==user.id
    result=await note_repo.get_notes()
    print(result)
    assert len(result) ==1
    assert result[0].title == "Title"
