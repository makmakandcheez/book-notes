from datetime import datetime

from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    body: str

class NoteUpdate(BaseModel):
    title: str | None = None
    body: str | None = None

class NoteResponse(BaseModel):
    id: int
    title: str
    body: str
    date_created: datetime
    date_updated: datetime
    user_id: int

    model_config = {"from_attributes": True}

