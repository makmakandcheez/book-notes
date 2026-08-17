# from passlib.context import CryptContext

from app.core.config import settings
from app.core.security import DUMMY_HASH, verify_password, get_password_hash, create_access_token, decode_access_token

from app.schemas.auth import Token
from app.schemas.user import UserCreate
from app.models.user import User
from app.repositories.user_repo import UserRepository

# from app.utils.hashing import hash_password, verify_password


class AuthService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo
        # self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    async def register(self, data: UserCreate) -> User:
        email = await self.repo.get_user_by_email(data.email)
        if email:
            raise ValueError("A user with this email already exists")
        username = await self.repo.filter_user(username=data.username)
        if username:
            raise ValueError("A user with this username already exists")
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=get_password_hash(data.password),
        )
        return await self.repo.create_user(user)



    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.repo.get_user_by_username(username)
        if not user:
            verify_password(password, DUMMY_HASH)
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


    async def logout_user(): pass


    async def refresh_token(): pass
    

    async def initiate_password_reset(): pass


    async def complete_password_reset(): pass