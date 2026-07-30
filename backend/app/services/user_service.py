from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate
from app.utils.hashing import hash_password


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register(self, data: UserCreate) -> User:
        email = await self.repo.get_by_email(data.email)
        if email:
            raise ValueError("A user with this email already exists")
        username = await self.repo.filter(username=data.username)
        if username:
            raise ValueError("A user with this username already exists")
        user = User(
            usr_username=data.username,
            usr_email=data.email,
            usr_hashed_password=hash_password(data.password),
        )
        return await self.repo.create(user)

    async def get_user(self, user_id: int) -> User | None:
        return await self.repo.get_by_id(user_id)

    async def filter_users(self, username: str | None = None) -> list[User]:
        return await self.repo.filter(username=username)

    async def delete_user(self, id: int) -> User | None:
        return await self.repo.delete(id)