from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note import Note


class NoteRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_note_by_id(self, id: UUID) -> Note | None:
        return await self.db.get(Note, id)

    async def get_notes(self) -> list[Note]:
        stmt = select(Note)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # add more complexity later
    async def filter_note(self, *,
                          user_id: UUID | None = None,
                          title: str | None = None,
                          is_public: bool | None = None) -> list[Note]:
        conditions = []
        stmt =select(Note)
        if user_id is not None:
            # append works because SQL objects overload == expression
            conditions.append(Note.user_id == user_id)
        if title is not None:
            conditions.append(Note.title == title)
        if is_public is not None:
            conditions.append(Note.is_public == is_public)
        stmt = select(Note).where(*conditions)
        stmt = stmt.order_by(Note.date_created.asc(),Note.title,Note.id.asc())
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
