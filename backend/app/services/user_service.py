# Things that manipulate an existing user.
from uuid import UUID
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self.repo.get_user_by_id(user_id)

    async def get_users(self, page: int, limit: int, *, username: str | None = None) -> list[User]:
        return await self.repo.get_users(offset=(page-1)*limit, limit=limit, username=username)

    async def filter_users(self, username: str | None = None) -> list[User]:
        return await self.repo.filter_user(username=username)

    async def update_user(self, user_id: UUID, data: UserUpdate, current_user: User) -> User | None:
        if user_id != current_user.id:
            raise PermissionError("Not authorized to update this user")
        new_data = data.model_dump(exclude_unset=True)
        user = await self.repo.update_user(user_id, new_data)
        return user

    async def delete_user(self, *, user_id: UUID, current_user: User) -> User | None:
        if user_id != current_user.id: # later add "and current_user.role != admin"
            raise PermissionError("Not authorized to delete this user")
        return await self.repo.delete_user(user_id)