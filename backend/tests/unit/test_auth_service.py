import pytest
import pytest_asyncio

from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate
from app.services.auth_service import AuthService


@pytest_asyncio.fixture
async def service(db):
    repo = UserRepository(db)
    return AuthService(repo)


@pytest.mark.asyncio
async def test_register_user(service):
    data = UserCreate(email="test@test.com", username="tester", password="1234")
    user = await service.register(data)
    assert user.usr_email == "test@test.com"
    assert user.usr_username == "tester"
    assert user.usr_hashed_password != "1234"


@pytest.mark.asyncio
async def test_register_duplicate_email(service):
    data = UserCreate(email="test@test.com", username="tester", password="1234")
    await service.register(data)
    with pytest.raises(ValueError, match="A user with this email already exists"):
        await service.register(data)


@pytest.mark.asyncio
async def test_register_duplicate_username(service):
    data = UserCreate(email="test@test.com", username="tester", password="1234")
    await service.register(data)
    dupe_data = UserCreate(email="new_email@test.com", username="tester", password="1234")
    with pytest.raises(ValueError, match="A user with this username already exists"):
        await service.register(dupe_data)


@pytest.mark.asyncio
async def test_authenticate_user(service):
    data = UserCreate(email="test@test.com", username="tester", password="1234")
    await service.register(data)
    user = await service.authenticate_user("tester", "1234")
    assert user.usr_email == "test@test.com"
    assert user.usr_username == "tester"
    assert user.usr_hashed_password != "1234"


@pytest.mark.asyncio
async def test_authenticate_wrong_username(service):
    data = UserCreate(email="test@test.com", username="tester", password="1234")
    await service.register(data)
    user = await service.authenticate_user("wrong_name", "1234")
    assert user is None



@pytest.mark.asyncio
async def test_authenticate_wrong_password(service):
    data = UserCreate(email="test@test.com", username="tester", password="1234")
    await service.register(data)
    user = await service.authenticate_user("tester", "wrong_pass")
    assert user is None