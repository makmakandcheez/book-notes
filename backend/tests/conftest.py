import os

os.environ.setdefault("SECRET_KEY", "test-key-this-is-not-real-its-for-testing")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./tests/test.db")

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    async_sessionmaker, 
    create_async_engine
)

from app.core.database import Base, get_db
from app.main import app

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

       