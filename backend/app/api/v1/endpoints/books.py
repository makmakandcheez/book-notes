from fastapi import APIRouter

router = APIRouter(
    prefix="/v1/books",
    tags=["books"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/")
async def get_all_books():
    return {"message": "Works!"}

@router.post("/")
async def add_book():
    return {"message": "Works!"}

@router.get("/{id}")
async def get_book(id: int):
    return {"message": "Works!",
            "id": id}

@router.put("/{id}")
async def update_book(id: int):
    return {"message": "Works!",
            "id": id}

@router.delete("/{id}")
async def delete_book(id: int):
    return {"message": "Works!",
            "id": id}

# Maybe more?