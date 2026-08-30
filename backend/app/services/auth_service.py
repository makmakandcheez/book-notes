# from passlib.context import CryptContext
from uuid import UUID

from app.core.security import (
    DUMMY_HASH,
    RefreshTokenData,
    TokenPair,
    create_access_token,
    create_jwt_refresh_token,
    decode_access_token,
    decode_refresh_token,
    get_password_hash,
    hash_refresh_token,
    verify_password,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.refresh_token_repo import RefreshTokenRepository
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate


class InvalidCredentialsError(Exception):
    pass
class InvalidRefreshTokenError(Exception):
    pass
class UserNotFoundError(Exception):
    pass

class AuthService:
    def __init__(self, user_repo: UserRepository, token_repo: RefreshTokenRepository) -> None:
        self.user_repo = user_repo
        self.token_repo = token_repo


    async def register(self, data: UserCreate) -> User:
        email = await self.user_repo.get_user_by_email(data.email)
        if email:
            raise ValueError("A user with this email already exists")
        username = await self.user_repo.filter_user(username=data.username)
        if username:
            raise ValueError("A user with this username already exists")
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=get_password_hash(data.password),
        )
        return await self.user_repo.create_user(user)

    async def authenticate_user_from_token(self, token: str) -> User:
        # raises jwt.InvalidTokenError if expired, or if signature not valid
        payload = decode_access_token(token)
        user_id = UUID(payload.get("sub"))
        user = await self.user_repo.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        return user


    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_repo.get_user_by_username(username)
        if not user:
            verify_password(password, DUMMY_HASH)
            raise InvalidCredentialsError("Incorrect username or password")
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Incorrect username or password")
        return user

    async def store_refresh_token(self, data: RefreshTokenData) -> RefreshToken:
        token = RefreshToken(
            jti=data.jti,
            user_id=data.user_id,
            token_hash=hash_refresh_token(data.token),
            expires_at=data.expires_at
        )
        token = await self.token_repo.create_refresh_token(token)
        return token

    async def login(self, username: str, password: str) -> TokenPair:
        user = await self.authenticate_user(username, password)
        access_token = create_access_token(user.id)
        refresh_token = create_jwt_refresh_token(user.id)
        await self.store_refresh_token(refresh_token)
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token.token
        )

    async def refresh_token(self, rt: str) -> TokenPair:
        # raises error if exp invalid
        payload = decode_refresh_token(rt)
        token = await self.token_repo.get_refresh_token_by_jti(UUID(payload["jti"]))
        if not token or token.revoked:
            raise InvalidRefreshTokenError("Invalid refresh token")
        await self.token_repo.revoke_refresh_token(token)
        new_access = create_access_token(token.user_id)
        new_rt = create_jwt_refresh_token(token.user_id)
        await self.store_refresh_token(new_rt)
        return TokenPair(access_token=new_access, refresh_token=new_rt.token)

    async def logout_user(): pass

    async def initiate_password_reset(): pass


    async def complete_password_reset(): pass
