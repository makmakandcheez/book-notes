# Things that manipulate an existing user.
from uuid import UUID
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self.repo.get_user_by_id(user_id)

    async def get_users(self, page: int, limit: int) -> list[User]:
        return await self.repo.get_users(offset=(page-1)*limit, limit=limit)

    async def filter_users(self, username: str | None = None) -> list[User]:
        return await self.repo.filter_user(username=username)

    async def delete_user(self, id: UUID) -> User | None:
        return await self.repo.delete_user(id)