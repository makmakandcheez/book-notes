from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query

from app.api.v1.dependencies import UserServiceDep, CurrentUserDep
from app.models.user import User
from app.schemas.user import UserPublic

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/", response_model=list[UserPublic])
async def get_users(
    service: UserServiceDep,
    username: str | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=0, le=10)] = 5
) -> list[UserPublic]:
    users = await service.get_users(page=page, limit=limit)
    return [UserPublic.model_validate(u) for u in users]


@router.get("/me", response_model=UserPublic)
async def read_users_me(current_user: CurrentUserDep) -> UserPublic:
    return current_user


@router.get("/{id}", response_model=UserPublic)
async def get_user(id: UUID, service: UserServiceDep) -> UserPublic:
    return await service.get_user_by_id(id)

@router.patch("/{id}")
async def update_user(
    id: UUID,
    service: UserServiceDep,
    current_user: CurrentUserDep) -> UserPublic:
    try:
        user = await service.update_user()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    

@router.delete("/{id}", response_model=UserPublic)
async def delete_user(id: UUID, service: UserServiceDep) -> UserPublic:
    user = await service.delete_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

    
