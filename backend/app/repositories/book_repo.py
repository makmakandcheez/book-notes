from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book

class BookRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, bk_id: int) -> Book:
        return await self.db.get(Book, bk_id)

    async def filter(self, *, title: str | None = None, author: str | None = None) -> list[Book]:
        stmt = select(Book)
        if title is not None:
            stmt = stmt.where(Book.bk_title == title)
        if author is not None:
            stmt = stmt.where(Book.bk_author == author)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())


    async def create(self, book: Book) -> Book:
        self.db.add(book)
        await self.db.flush()
        return book


    async def delete(self, id: int) -> Book:
        book = await self.get_by_id(id)
        if book:
            await self.db.delete(book)
            await self.db.flush()
        return book

