from uuid import UUID
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from app.models.note import Note

class NoteRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_note_by_id(self, id: UUID) -> Note | None:
        return await self.db.get(Note, id)

    async def filter_note(self, *, title: str | None = None) -> list[Note]:
        stmt = select(Note)
        if title is not None:
            stmt = stmt.where(Note.title == title)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_note(self, note: Note) -> Note:
        self.db.add(note)
        await self.db.flush()
        return note

    # need to update all functions to receive id's and not ORM instances
    async def update_note(self, note: Note, data: dict) -> Note:
        for key, value in data.items():
            setattr(note, key, value)
        note.date_updated = func.now()
        await self.db.flush()
        await self.db.refresh(note)


    async def delete_note(self, note: Note) -> Note | None:
        if note:
            await self.db.delete(note)
            await self.db.flush()
        return note
    