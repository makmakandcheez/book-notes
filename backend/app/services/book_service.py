from app.models.book import Book
from app.repositories.book_repo import BookRepository
from app.schemas.book import BookCreate


class BookService:
    def __init__(self, repo: BookRepository) -> None:
        self.repo = repo

    async def add_book(self, data: BookCreate) -> Book:
        book = Book(
            bk_title=data.bk_title,
            bk_author=data.bk_author,
            bk_rating=data.bk_rating
        )
        return await self.repo.create(book)

    async def list_books(self) -> list[Book]:
        return await self.repo.list_all()

    async def filter_books(self, title: str | None = None, author: str | None = None) -> list[Book]:
        return await self.repo.filter(title=title, author=author)

    async def get_by_id(self, id: int) -> Book:
        return await self.repo.get_by_id(id)

    async def delete_book(self, id: int) -> Book:
        return await self.repo.delete(id)