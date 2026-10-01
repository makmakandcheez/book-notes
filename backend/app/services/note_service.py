from uuid import UUID

from app.models.note import Note
from app.repositories.note_repo import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, note_repo: NoteRepository) -> None:
        self.note_repo = note_repo

    async def add_note(self, data: NoteCreate, user_id: UUID) -> Note:
        note = Note(title=data.title, body=data.body, is_public=data.is_public, user_id=user_id)
        return await self.note_repo.create_note(note)

    async def get_user_public_notes(self, user_id: UUID) -> list[Note]:
        notes = await self.note_repo.filter_note(user_id=user_id, is_public=True)
        return notes

    async def filter_notes(
        self,
        *,
        title: str | None = None,
        user_id: UUID | None = None,
        is_public: bool | None = None,
        requesting_user_id: UUID | None = None,
    ) -> list[Note]:
        # Only the note owner can see their own private notes.
        is_own_notes = user_id is not None and user_id == requesting_user_id
        if is_own_notes:
            return await self.note_repo.filter_note(
                user_id=user_id, title=title, is_public=is_public
            )
        return await self.note_repo.filter_note(user_id=user_id, title=title, is_public=True)

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

    async def delete_note(self, id: UUID, user_id: UUID) -> Note | None:
        note = await self.note_repo.get_note_by_id(id)
        if note is None:
            return None
        if note.user_id != user_id:
            raise PermissionError("Not authorized to delete this note")
        return await self.note_repo.delete_note(note)
