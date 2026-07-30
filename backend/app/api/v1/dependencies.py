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


from app.repositories.note_repo import NoteRepository
from app.services.note_service import NoteService

def get_note_repository(db: DbSession) -> NoteRepository:
    return NoteRepository(db)

NoteRepositoryDep = Annotated[NoteRepository, Depends(get_note_repository)]

def get_note_service(repo: NoteRepositoryDep) -> NoteService:
    return NoteService(repo)

NoteServiceDep = Annotated[NoteService, Depends(get_note_service)]


from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService

def get_user_repository(db: DbSession) -> UserRepository:
    return UserRepository(db)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]

def get_user_service(repo: UserRepositoryDep) -> UserService:
    return UserService(repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]