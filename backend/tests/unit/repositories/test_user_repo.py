import pytest
import pytest_asyncio

from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.core.security import get_password_hash, verify_password


@pytest.mark.asyncio
async def test_create_user(user_repo):
    data = User(username="John", email="test@test.com", hashed_password=get_password_hash("123"))
    user = await user_repo.create_user(data)
    assert user.username == "John"
    assert user.email == "test@test.com"
    assert verify_password("123", user.hashed_password)


@pytest.mark.asyncio
async def test_create_user_unique_uuid(user_repo):
    data = User(username="John", email="test@test.com", hashed_password = get_password_hash("123"))
    user = await user_repo.create_user(data)
    uuid_1 = user.id

    data = User(username="Guy", email="example@test.com", hashed_password = get_password_hash("123"))
    user = await user_repo.create_user(data)

    assert user.id != uuid_1


@pytest.mark.asyncio
async def test_get_users(user_repo):
    users = [
        User(username=f"user{i}", email=f"{i}@test.com", hashed_password = get_password_hash("123"))
        for i in range(1, 11)
    ]
    for user in users:
        await user_repo.create_user(user)

    result = await user_repo.get_users(offset=0, limit=5)
    assert len(result) == 5
    assert [user.username for user in result] == [
        "user1",
        "user2",
        "user3",
        "user4",
        "user5"
    ]
    assert ("user6" or "user7" or "user8" or "user9" or "user10") not in result


@pytest.mark.asyncio
async def test_get_users_with_offset(user_repo):
    users = [
        User(username=f"user{i}", email=f"{i}@test.com", hashed_password = get_password_hash("123"))
        for i in range(1, 11)
    ]
    for user in users:
        await user_repo.create_user(user)

    result = await user_repo.get_users(offset=5, limit=5)
    assert len(result) == 5
    assert [user.username for user in result] == [
        "user6",
        "user7",
        "user8",
        "user9",
        "user10"
    ]
    assert ("user1" or "user2" or "user3" or "user4" or "user5") not in result


@pytest.mark.asyncio
async def test_get_users_with_offset_out_of_bounds(user_repo):
    users = [
        User(username=f"user{i}", email=f"{i}@test.com", hashed_password = get_password_hash("123"))
        for i in range(1, 11)
    ]
    for user in users:
        await user_repo.create_user(user)

    result = await user_repo.get_users(offset=10, limit=5)
    assert len(result) == 0


@pytest.mark.asyncio
async def test_get_users_with_large_limit(user_repo):
    users = [
        User(username=f"user{i}", email=f"{i}@test.com", hashed_password = get_password_hash("123"))
        for i in range(1, 11)
    ]
    for user in users:
        await user_repo.create_user(user)

    result = await user_repo.get_users(offset=0, limit=30)
    assert len(result) == 10
    assert [user.username for user in result] == [
        "user1",
        "user2",
        "user3",
        "user4",
        "user5",
        "user6",
        "user7",
        "user8",
        "user9",
        "user10"
    ]