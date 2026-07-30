from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note import Note

class NoteRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, id: int) -> Note | None:
        return await self.db.get(Note, id)

    async def filter(self, *, title: str | None = None) -> list[Note]:
        stmt = select(Note)
        if title is not None:
            stmt = stmt.where(Note.nt_title == title)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, note: Note) -> Note:
        self.db.add(note)
        await self.db.flush()
        return note

    async def delete(self, id: int) -> Note | None:
        note = await self.get_by_id(id)
        if note:
            await self.db.delete(note)
            await self.db.flush()
        return note
    