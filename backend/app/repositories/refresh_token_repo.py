from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        self.db.add(refresh_token)
        await self.db.flush()
        return refresh_token

    async def get_refresh_token_by_jti(self, jti: UUID) -> RefreshToken:
        return await self.db.get(RefreshToken, jti)

    async def get_refresh_token_by_token_hash(self, token_hash: str) -> RefreshToken:
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        if refresh_token:
            refresh_token.revoked = True
            await self.db.flush()
        return refresh_token

    async def delete_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        if refresh_token:
            await self.db.delete(refresh_token)
            await self.db.flush()
        return refresh_token
