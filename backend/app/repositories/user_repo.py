from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        return user

    async def filter_user(self, *, username: str | None = None) -> list[User]:
        stmt = select(User)
        if username is not None:
            stmt = stmt.where(User.username == username)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update_user_username(self, user: User, username: str) -> User:
        pass

    async def delete_user(self, id: int) -> User:
        user = await self.get_user_by_id(id)
        if user:
            await self.db.delete(user)
            await self.db.flush()
        return user