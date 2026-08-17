import pytest
import pytest_asyncio

from app.repositories.note_repo import NoteRepository
from app.repositories.user_repo import UserRepository
from app.schemas.note import NoteCreate, NoteUpdate
from app.schemas.user import UserCreate
from app.services.note_service import NoteService
from app.services.auth_service import AuthService


@pytest_asyncio.fixture
async def note_service(db):
    repo = NoteRepository(db)
    return NoteService(repo)

@pytest_asyncio.fixture
async def auth_service(db):
    repo = UserRepository(db)
    return AuthService(repo)


@pytest.mark.asyncio
async def test_create_note(note_service, auth_service):
    data = UserCreate(email="test@test.com", username="tester", password="1234")
    await auth_service.register(data)


    note = NoteCreate(
        title="Test Title",
        body="Test body",
    )

    note = await note_service.add_note(note, 1)
    assert note.title == "Test Title"
    assert note.body == "Test body"
    assert note.user_id == 1


@pytest.mark.asyncio
async def test_update_note(note_service, auth_service):
    data = UserCreate(email="test@test.com", username="tester", password="1234")
    await auth_service.register(data)

    note = NoteCreate(
        title="Test Title",
        body="Test body",
    )
    await note_service.add_note(note, 1)
    new_note = NoteUpdate(
        body="Body update"
    )

    note = await note_service.update_note(1, new_note, 1)
    assert note.title == "Test Title"
    assert note.body == "Body update"
    assert note.user_id == 1