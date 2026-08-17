import pytest
import pytest_asyncio

from app.repositories.note_repo import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate
from app.services.note_service import NoteService



@pytest_asyncio.fixture
async def note_service(db):
    repo = NoteRepository(db)
    return NoteService(repo)




@pytest.mark.asyncio
async def test_create_note(note_service, create_user):
    note = NoteCreate(
        title="Test Title",
        body="Test body",
    )

    note = await note_service.add_note(note, create_user.id)
    assert note.title == "Test Title"
    assert note.body == "Test body"
    assert note.user_id == create_user.id


@pytest.mark.asyncio
async def test_update_note(note_service, create_user):
    data = NoteCreate(
        title="Test Title",
        body="Test body",
    )
    note = await note_service.add_note(data, create_user.id)
    new_data = NoteUpdate(
        body="Body update"
    )
    old_note_id = note.id
    note = await note_service.update_note(note.id, new_data, create_user.id)
    assert note.id == old_note_id
    assert note.title == "Test Title"
    assert note.body == "Body update"
    assert note.user_id == create_user.id