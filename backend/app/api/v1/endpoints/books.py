from fastapi import APIRouter

router = APIRouter(
    prefix="/v1/books",
    tags=["books"],
    responses={404: {"description": "Not Found"}},
)

@router.get("/")
async def get_all_books():
    return set

@router.post("/")
async def add_book():
    return 

@router.get("/{id}")
async def get_book(id: int):
    return

@router.put("/{id}")
async def update_book(id: int):
    return

@router.delete("/{id}")
async def delete_book(id: int):
    return

# Maybe more?