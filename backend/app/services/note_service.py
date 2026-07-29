from app.models.note import Note
from app.repositories.note_repo import NoteRepository
from app.schemas.note import NoteCreate


class NoteService:
    def __init__(self, repo: NoteRepository) -> None:
        self.repo = repo

    async def add_note(self, data: NoteCreate) -> Note:
        note = Note(
            nt_title=data.title,
            nt_body=data.body
        )
        return await self.repo.create(note)

    async def filter_notes(self, title: str | None = None) -> list[Note]:
        return await self.repo.filter(title=title)

    async def get_by_id(self, id: int) -> Note:
        return await self.repo.get_by_id(id)

    async def delete_note(self, id: int) -> Note:
        return await self.repo.delete(id)