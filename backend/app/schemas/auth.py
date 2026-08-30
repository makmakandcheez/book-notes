import uuid
from enum import StrEnum

from pydantic import BaseModel


class TokenType(StrEnum):
    BEARER = "bearer"


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = TokenType.BEARER

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    user_id: uuid.UUID
