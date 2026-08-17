from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import Book

class BookRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, book_id: int) -> Book | None:
        return await self.db.get(Book, book_id)

    async def filter(self, *, title: str | None = None, author: str | None = None) -> list[Book]:
        stmt = select(Book)
        if title is not None:
            stmt = stmt.where(Book.title == title)
        if author is not None:
            stmt = stmt.where(Book.author == author)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())


    async def create(self, book: Book) -> Book:
        self.db.add(book)
        await self.db.flush()
        return book


    async def delete(self, id: int) -> Book | None:
        book = await self.get_by_id(id)
        if book:
            await self.db.delete(book)
            await self.db.flush()
        return book

