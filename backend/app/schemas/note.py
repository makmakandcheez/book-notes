import uuid
from datetime import datetime

from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    body: str
    is_public: bool = False

class NoteUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    is_public: bool | None = None

class NoteResponse(BaseModel):
    id: uuid.UUID
    title: str
    body: str
    is_public: bool
    date_created: datetime
    date_updated: datetime
    user_id: uuid.UUID

    model_config = {"from_attributes": True}

