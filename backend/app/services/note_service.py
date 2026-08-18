from uuid import UUID
from app.models.note import Note
from app.repositories.note_repo import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, repo: NoteRepository) -> None:
        self.repo = repo

    async def add_note(self, data: NoteCreate, user_id: UUID) -> Note:
        note = Note(
            title=data.title,
            body=data.body,
            user_id=user_id
        )
        return await self.repo.create_note(note)


    async def filter_notes(self, title: str | None = None) -> list[Note]:
        return await self.repo.filter_note(title=title)

    async def get_by_id(self, id: UUID) -> Note:
        return await self.repo.get_note_by_id(id)

    async def update_note(self, note_id: UUID, data: NoteUpdate, user_id: UUID) -> Note:
        note = await self.repo.get_note_by_id(note_id)
        if note.user_id != user_id:
            # Need to change this. This is not a value error its an authorization error.
            raise ValueError("This is not your note.")
        new_data = data.model_dump(exclude_unset=True)
        await self.repo.update_note(note, new_data)
        return note

    async def delete_note(self, id: UUID) -> Note:
        note = await self.repo.get_note_by_id(id)
        return await self.repo.delete_note(note)