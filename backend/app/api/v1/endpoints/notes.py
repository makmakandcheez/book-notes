from fastapi import APIRouter

router = APIRouter(
    prefix="/v1/notes",
    tags=["notes"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/")
async def get_all_notes():
    return {"message": "Works!"}

@router.post("/")
async def create_note():
    return {"message": "Works!"}

@router.get("/{id}")
async def retrieve_note(id: int):
    return {"message": "Works!",
            "id": id}

@router.put("/{id}")
async def update_note(id: int):
    return {"message": "Works!",
            "id": id}

@router.delete("/{id}")
async def delete_note(id: int):
    return {"message": "Works!",
            "id": id}

