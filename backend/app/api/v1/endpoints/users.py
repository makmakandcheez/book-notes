from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, status

from app.api.v1.dependencies import UserServiceDep, CurrentUserDep, NoteServiceDep
from app.models.user import User
from app.schemas.user import UserPublic, UserUpdate
from app.schemas.note import NoteResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserPublic])
async def get_users(
    service: UserServiceDep,
    username: str | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=10)] = 5
) -> list[UserPublic]:
    users = await service.get_users(page=page, limit=limit, username=username)
    return [UserPublic.model_validate(u) for u in users]


@router.get("/me", response_model=UserPublic)
async def read_users_me(current_user: CurrentUserDep) -> UserPublic:
    return current_user


@router.get("/{id}", response_model=UserPublic)
async def get_user(id: UUID, service: UserServiceDep) -> UserPublic:
    try:
        user = await service.get_user_by_id(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserPublic.model_validate(user)

@router.get("/{id}/notes")
async def get_user_public_notes(
    id: UUID,
    note_service: NoteServiceDep
) -> list[NoteResponse]:
    notes = await note_service.get_user_public_notes(id)
    return [NoteResponse.model_validate(n) for n in notes]


@router.patch("/{id}")
async def update_user(
    id: UUID,
    data: UserUpdate,
    service: UserServiceDep,
    current_user: CurrentUserDep
) -> UserPublic:
    try:
        user = await service.update_user(id, data, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserPublic.model_validate(user)   




# Setting status_code=204 is good if no content, but I do want to return the deleted user, so it stays 200.
@router.delete("/{id}", response_model=UserPublic)
async def delete_user(
    id: UUID, 
    service: UserServiceDep,
    current_user: CurrentUserDep
) -> UserPublic:
    try:
        user = await service.delete_user(user_id=id, current_user=current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

    
