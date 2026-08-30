from app.models.book import Book
from app.repositories.book_repo import BookRepository
from app.schemas.book import BookCreate


class BookService:
    def __init__(self, repo: BookRepository) -> None:
        self.repo = repo

    async def add_book(self, data: BookCreate) -> Book:
        book = Book(
            title=data.title,
            author=data.author,
            rating=data.rating
        )
        return await self.repo.create(book)

    async def filter_books(self, title: str | None = None, author: str | None = None) -> list[Book]:
        return await self.repo.filter(title=title, author=author)

    async def get_by_id(self, id: int) -> Book:
        return await self.repo.get_by_id(id)

    async def delete_book(self, id: int) -> Book:
        return await self.repo.delete(id)
