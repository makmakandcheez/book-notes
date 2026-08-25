from uuid import uuid4

import pytest
import pytest_asyncio

from app.core.security import create_jwt_refresh_token
from app.schemas.user import UserCreate
from app.services.auth_service import InvalidCredentialsError, InvalidRefreshTokenError


@pytest_asyncio.fixture
def user_data():
    return UserCreate(email="test@test.com", username="tester", password="1234")


@pytest.mark.asyncio
async def test_register_user(auth_service, user_data):
    user = await auth_service.register(user_data)
    assert user.email == "test@test.com"
    assert user.username == "tester"
    assert user.hashed_password != "1234"


@pytest.mark.asyncio
async def test_register_duplicate_email(auth_service, user_data):
    await auth_service.register(user_data)
    with pytest.raises(ValueError, match="A user with this email already exists"):
        await auth_service.register(user_data)


@pytest.mark.asyncio
async def test_register_duplicate_username(auth_service, user_data):
    await auth_service.register(user_data)
    dupe_data = UserCreate(email="new_email@test.com", username="tester", password="1234")
    with pytest.raises(ValueError, match="A user with this username already exists"):
        await auth_service.register(dupe_data)


@pytest.mark.asyncio
async def test_authenticate_user(auth_service, user_data):
    await auth_service.register(user_data)
    user = await auth_service.authenticate_user("tester", "1234")
    assert user.email == "test@test.com"
    assert user.username == "tester"
    assert user.hashed_password != "1234"


@pytest.mark.asyncio
async def test_authenticate_wrong_username(auth_service, user_data):
    await auth_service.register(user_data)
    with pytest.raises(InvalidCredentialsError, match="Incorrect username or password"):
        await auth_service.authenticate_user("wrong_name", "1234")



@pytest.mark.asyncio
async def test_authenticate_wrong_password(auth_service, user_data):
    await auth_service.register(user_data)
    with pytest.raises(InvalidCredentialsError, match="Incorrect username or password"):
        await auth_service.authenticate_user("tester", "wrong_pass")


@pytest.mark.asyncio
async def test_store_refresh_token(auth_service):
    user_id = uuid4()
    token_data = create_jwt_refresh_token(user_id)
    token = await auth_service.store_refresh_token(token_data)
    assert token and token.user_id == user_id