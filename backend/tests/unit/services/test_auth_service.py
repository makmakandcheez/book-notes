import pytest
import pytest_asyncio


from app.schemas.user import UserCreate


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
    user = await auth_service.authenticate_user("wrong_name", "1234")
    assert user is None



@pytest.mark.asyncio
async def test_authenticate_wrong_password(auth_service, user_data):
    await auth_service.register(user_data)
    user = await auth_service.authenticate_user("tester", "wrong_pass")
    assert user is None