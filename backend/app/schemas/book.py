from pydantic import BaseModel

# the request body for creating a book
class BookCreate(BaseModel):
    title: str
    author: str
    rating: float | None = None
    # img_url: str | None = None
    # date_published: str | None = None



class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    rating: float | None = None

    model_config = {"from_attributes": True}