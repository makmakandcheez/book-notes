from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.usr_email == email))
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        return user

    async def filter(self, *, username: str | None = None) -> list[User]:
        stmt = select(User)
        if username is not None:
            stmt = stmt.where(User.usr_username == username)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def delete(self, id: int) -> User:
        user = await self.get_by_id(id)
        if user:
            await self.db.delete(user)
            await self.db.flush()
        return user