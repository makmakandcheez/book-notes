from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.repositories.book_repo import BookRepository
from app.repositories.note_repo import NoteRepository
from app.repositories.refresh_token_repo import RefreshTokenRepository
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService
from app.services.book_service import BookService
from app.services.note_service import NoteService
from app.services.user_service import UserService

# Database
DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_book_repository(db: DbSession) -> BookRepository:
    return BookRepository(db)

BookRepositoryDep = Annotated[BookRepository, Depends(get_book_repository)]

def get_book_service(repo: BookRepositoryDep) -> BookService:
    return BookService(repo)

BookServiceDep = Annotated[BookService, Depends(get_book_service)]


def get_note_repository(db: DbSession) -> NoteRepository:
    return NoteRepository(db)

NoteRepositoryDep = Annotated[NoteRepository, Depends(get_note_repository)]

def get_note_service(repo: NoteRepositoryDep) -> NoteService:
    return NoteService(repo)

NoteServiceDep = Annotated[NoteService, Depends(get_note_service)]


def get_user_repository(db: DbSession) -> UserRepository:
    return UserRepository(db)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]

def get_user_service(repo: UserRepositoryDep) -> UserService:
    return UserService(repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_refresh_token_repositoory(db: DbSession) -> RefreshTokenRepository:
    return RefreshTokenRepository(db)

RefreshTokenRepoDep = Annotated[RefreshTokenRepository, Depends(get_refresh_token_repositoory)]

def get_auth_service(user_repo: UserRepositoryDep, token_repo: RefreshTokenRepoDep) -> AuthService:
    return AuthService(user_repo=user_repo, token_repo=token_repo)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


### Authorization

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token"
)

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_service: AuthServiceDep
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = await auth_service.authenticate_user_from_token(token)
    except (InvalidTokenError) as e:
        raise credentials_exception from e
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]

# def get_current_active_user
