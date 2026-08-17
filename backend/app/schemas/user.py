from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    model_config = {"from_attributes": True}


class UserPrivate(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}
