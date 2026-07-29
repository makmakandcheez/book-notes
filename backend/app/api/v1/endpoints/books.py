from fastapi import APIRouter, HTTPException

from app.api.v1.dependencies import BookServiceDep
from app.schemas.book import BookCreate, BookResponse

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(data: BookCreate, service: BookServiceDep) -> BookResponse:
    try:
        book = await service.add_book(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return BookResponse.model_validate(book)


@router.get("/", response_model=list[BookResponse])
async def get_books(
    service: BookServiceDep,
    title: str | None = None,
    author: str | None = None
) -> list[BookResponse]:
    books = await service.filter_books(title=title, author=author)
    return [BookResponse.model_validate(b) for b in books]


@router.get("/{id}", response_model=BookResponse)
async def get_book(id: int, service: BookServiceDep):
    return await service.get_by_id(id)

@router.put("/{id}")
async def update_book(id: int):
    return {"message": "Works!",
            "id": id}

@router.delete("/{id}", response_model=BookResponse)
async def delete_book(id: int, service: BookServiceDep):
    book = await service.delete_book(id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Maybe more?