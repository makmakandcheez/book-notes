import os

os.environ.setdefault("SECRET_KEY", "test-key-this-is-not-real-its-for-testing")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./tests/test.db")

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base, get_db
from app.main import app
from app.repositories.note_repo import NoteRepository
from app.repositories.refresh_token_repo import RefreshTokenRepository
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate
from app.services.auth_service import AuthService
from app.services.user_service import UserService

TEST_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_async_engine(TEST_DATABASE_URL)
TestSession = async_sessionmaker(engine, expire_on_commit=False)


async def override_get_db():
    async with TestSession() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@pytest_asyncio.fixture(autouse=True, scope="session")
async def _override_dependencies():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def db() -> AsyncSession: # type: ignore
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestSession() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db) -> AsyncClient: # type: ignore
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


#-----------------------
@pytest_asyncio.fixture
async def user_repo(db):
    return UserRepository(db)

@pytest_asyncio.fixture
async def note_repo(db):
    return NoteRepository(db)

@pytest_asyncio.fixture
async def refresh_token_repo(db):
    return RefreshTokenRepository

@pytest_asyncio.fixture
async def auth_service(db):
    user_repo = UserRepository(db)
    rt_repo = RefreshTokenRepository(db)
    return AuthService(user_repo=user_repo, token_repo=rt_repo)

@pytest_asyncio.fixture
async def user_service(db):
    repo = UserRepository(db)
    return UserService(repo)


@pytest_asyncio.fixture
async def create_user(auth_service):
    data = UserCreate(email="test@test.com", username="tester", password="1234")
    user = await auth_service.register(data)
    return user



@pytest_asyncio.fixture
async def auth_token(client):
    await client.post(
        "api/v1/auth/signup",
        json={
            "email": "test@example.com",
            "username": "Johnny",
            "password": "123"
            },
    )

    response = await client.post(
        "api/v1/auth/token",
        data={
            "username": "Johnny",
            "password": "123"
            },
    )

    return response.json()["access_token"]

