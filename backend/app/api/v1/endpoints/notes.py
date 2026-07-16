from fastapi import APIRouter

router = APIRouter(
    prefix="v1/notes",
    tages=["notes"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/")
async def get_all_notes():
    return

@router.post("/")
async def create_note():
    return

@router.get("/{id}")
async def retrieve_note(id: int):
    return

@router.put("/{id}")
async def update_note(id: int):
    return

@router.delete("/{id}")
async def delete_note(id: int):
    return

