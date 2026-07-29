from pydantic import BaseModel

# the request body for creating a book
class BookCreate(BaseModel):
    bk_title: str
    bk_author: str
    bk_rating: float | None = None
    # img_url: str | None = None
    # date_published: str | None = None



class BookResponse(BaseModel):
    bk_id: int
    bk_title: str
    bk_author: str
    bk_rating: float | None = None

    model_config = {"from_attributes": True}