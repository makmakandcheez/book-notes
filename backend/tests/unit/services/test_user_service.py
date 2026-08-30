import pytest

from app.core.security import get_password_hash
from app.models.user import User


@pytest.mark.asyncio
async def test_get_users(user_service, user_repo):
    users = [
        User(username=f"user{i}", email=f"{i}@test.com", hashed_password = get_password_hash("123"))
        for i in range(1, 11)
    ]
    for user in users:
        await user_repo.create_user(user)

    result = await user_service.get_users(page=1, limit=5)
    assert len(result) == 5
    assert [user.username for user in result] == [
        "user1",
        "user2",
        "user3",
        "user4",
        "user5"
    ]
    assert ("user6" and "user7" and "user8" and "user9" and "user10") not in result


@pytest.mark.asyncio
async def test_get_users_page_2(user_service, user_repo):
    users = [
        User(username=f"user{i}", email=f"{i}@test.com", hashed_password = get_password_hash("123"))
        for i in range(1, 11)
    ]
    for user in users:
        await user_repo.create_user(user)

    result = await user_service.get_users(page=2, limit=5)
    assert len(result) == 5
    assert [user.username for user in result] == [
            "user6",
            "user7",
            "user8",
            "user9",
            "user10"
        ]
    assert ("user1" and "user2" and "user3" and "user4" and "user5") not in result


@pytest.mark.asyncio
async def test_get_users_page_out_of_bounds(user_service, user_repo):
    users = [
        User(username=f"user{i}", email=f"{i}@test.com", hashed_password = get_password_hash("123"))
        for i in range(1, 11)
    ]
    for user in users:
        await user_repo.create_user(user)

    result = await user_service.get_users(page=3, limit=5)
    assert len(result) == 0
