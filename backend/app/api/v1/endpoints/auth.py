from typing import Annotated

from jwt import InvalidTokenError

from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependencies import AuthServiceDep
from app.services.auth_service import InvalidCredentialsError, InvalidRefreshTokenError

from app.schemas.user import UserCreate, UserPublic
from app.schemas.auth import TokenResponse, RefreshTokenRequest


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


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep
) -> TokenResponse:
    try:
        tokens = await auth_service.login(form_data.username, form_data.password)
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        ) from e
    response = TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type="bearer"
    )
    return TokenResponse.model_validate(response)
        

@router.post("/refresh-token", response_model=TokenResponse)
async def refresh(
    rt: RefreshTokenRequest,
    auth_service: AuthServiceDep
) -> TokenResponse:
    try:
        tokens = await auth_service.refresh_token(rt.refresh_token)
    except (InvalidTokenError, InvalidRefreshTokenError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        ) from e
    response = TokenResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        token_type="bearer"
    )
    return TokenResponse.model_validate(response)