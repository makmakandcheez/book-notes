from fastapi import APIRouter, HTTPException

from app.api.v1.dependencies import UserServiceDep
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(data: UserCreate, service: UserServiceDep) -> UserResponse:
    try:
        user = await service.register(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return UserResponse.model_validate(user)


@router.get("/", response_model=list[UserResponse])
async def get_users(
    service: UserServiceDep,
    username: str | None = None
) -> list[UserResponse]:
    users = await service.filter_users(username=username)
    return [UserResponse.model_validate(u) for u in users]


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, service: UserServiceDep) -> UserResponse:
    return await service.get_user(id)

@router.put("/{id}")
async def update_book(id: int):
    return {"message": "Works!",
            "id": id}

@router.delete("/{id}", response_model=UserResponse)
async def delete_book(id: int, service: UserServiceDep):
    user = await service.delete_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user