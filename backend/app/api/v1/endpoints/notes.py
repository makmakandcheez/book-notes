from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from app.api.v1.dependencies import NoteServiceDep, CurrentUserDep
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate
from app.models.user import User

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/", response_model=list[NoteResponse])
async def get_notes(
    service: NoteServiceDep,
    title: str | None = None
) -> list[NoteResponse]:
    notes = await service.filter_notes(title=title)
    return [NoteResponse.model_validate(n) for n in notes]

@router.post("/", response_model=NoteResponse, status_code=201)
async def create_note(
    data: NoteCreate, 
    service: NoteServiceDep, 
    current_user: CurrentUserDep
) -> NoteResponse:
    try:
        note = await service.add_note(data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return NoteResponse.model_validate(note)

@router.get("/{id}", response_model=NoteResponse)
async def get_note(id: int, service: NoteServiceDep) -> NoteResponse:
    try:
        note = await service.get_by_id(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return NoteResponse.model_validate(note)



@router.patch("/{id}", response_model=NoteResponse)
async def update_note(
    id: int,
    data: NoteUpdate, 
    service: NoteServiceDep,
    current_user: CurrentUserDep
) -> NoteResponse:
    try:
        note = await service.update_note(id, data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return NoteResponse.model_validate(note)


@router.delete("/{id}", response_model=NoteResponse)
async def delete_note(
    id: int, 
    service: NoteServiceDep
    ) -> NoteResponse:
    note = await service.delete_note(id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


