from datetime import datetime

from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    body: str


class NoteResponse(BaseModel):
    nt_id: int
    nt_title: str
    nt_body: str
    nt_date_created: datetime
    nt_date_updated: datetime

    model_config = {"from_attributes": True}

