import uuid

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str


class UserPublic(BaseModel):
    id: uuid.UUID
    username: str
    model_config = {"from_attributes": True}


class UserPrivate(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}
