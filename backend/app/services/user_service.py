# Things that manipulate an existing user.

from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.repo.get_user_by_id(user_id)

    async def filter_users(self, username: str | None = None) -> list[User]:
        return await self.repo.filter_user(username=username)

    async def delete_user(self, id: int) -> User | None:
        return await self.repo.delete_user(id)