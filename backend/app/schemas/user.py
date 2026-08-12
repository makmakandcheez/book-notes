from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserPublic(BaseModel):
    usr_id: int
    usr_username: str
    model_config = {"from_attributes": True}


class UserPrivate(BaseModel):
    usr_id: int
    usr_username: str
    usr_email: EmailStr

    model_config = {"from_attributes": True}
