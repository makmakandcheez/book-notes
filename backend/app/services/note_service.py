from uuid import UUID

from app.models.note import Note
from app.repositories.note_repo import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, note_repo: NoteRepository) -> None:
        self.note_repo = note_repo

    async def add_note(self, data: NoteCreate, user_id: UUID) -> Note:
        note = Note(
            title=data.title,
            body=data.body,
            is_public=data.is_public,
            user_id=user_id
        )
        return await self.note_repo.create_note(note)

    async def get_user_public_notes(self, user_id: UUID) -> list[Note]:
        notes = await self.note_repo.filter_note(user_id=user_id, is_public=True)
        return notes

    async def filter_notes(self, title: str | None = None) -> list[Note]:
        return await self.note_repo.filter_note(title=title)

    async def get_by_id(self, id: UUID) -> Note:
        return await self.note_repo.get_note_by_id(id)

    async def update_note(self, note_id: UUID, data: NoteUpdate, user_id: UUID) -> Note:
        note = await self.note_repo.get_note_by_id(note_id)
        if note.user_id != user_id:
            # Need to change this. This is not a value error its an authorization error.
            raise ValueError("This is not your note.")
        new_data = data.model_dump(exclude_unset=True)
        await self.note_repo.update_note(note, new_data)
        return note

    async def delete_note(self, id: UUID) -> Note:
        note = await self.note_repo.get_note_by_id(id)
        return await self.note_repo.delete_note(note)
