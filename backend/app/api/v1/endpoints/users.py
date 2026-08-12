from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from app.api.v1.dependencies import UserServiceDep, get_current_user
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
    username: str | None = None
) -> list[UserPublic]:
    users = await service.filter_users(username=username)
    return [UserPublic.model_validate(u) for u in users]


@router.get("/me", response_model=UserPublic)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> UserPublic:
    return current_user


@router.get("/{id}", response_model=UserPublic)
async def get_user(id: int, service: UserServiceDep) -> UserPublic:
    return await service.get_user_by_id(id)

@router.put("/{id}")
async def update_book(id: int):
    return {"message": "Works!",
            "id": id}

@router.delete("/{id}", response_model=UserPublic)
async def delete_user(id: int, service: UserServiceDep) -> UserPublic:
    user = await service.delete_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

    
