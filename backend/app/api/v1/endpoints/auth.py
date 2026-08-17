from typing import Annotated

from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependencies import AuthServiceDep

from app.core.security import create_access_token

from app.schemas.user import UserCreate, UserPublic
from app.schemas.auth import Token


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/signup", response_model=UserPublic, status_code=201)
async def create_user(data: UserCreate, service: AuthServiceDep) -> UserPublic:
    try:
        user = await service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return UserPublic.model_validate(user)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep
) -> Token:
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    return Token(access_token=access_token, token_type="bearer")