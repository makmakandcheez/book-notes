from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.repositories.book_repo import BookRepository
from app.services.book_service import BookService

# Database
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


from app.services.auth_service import AuthService

def get_auth_service(repo: UserRepositoryDep) -> AuthService:
    return AuthService(repo)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


### Authorization
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token"
)

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: UserServiceDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Coud not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = UUID(user_id)
    except (InvalidTokenError, ValueError, TypeError):
        raise credentials_exception

    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]

# def get_current_active_user