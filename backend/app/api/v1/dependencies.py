from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.book_repo import BookRepository
from app.services.book_service import BookService

DbSession = Annotated[AsyncSession, Depends(get_db)]

def get_book_repository(db: DbSession) -> BookRepository:
    return BookRepository(db)

BookRepositoryDep = Annotated[BookRepository, Depends(get_book_repository)]

def get_book_service(repo: BookRepositoryDep) -> BookService:
    return BookService(repo)

BookServiceDep = Annotated[BookService, Depends(get_book_service)]
