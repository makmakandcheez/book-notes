from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.core.database import Base

class Note(Base):
    __tablename__ = "notes"

    nt_id: Mapped[int] = mapped_column(primary_key=True)
    nt_title: Mapped[str] = mapped_column(String(100), nullable=False)
    nt_body: Mapped[str] = mapped_column(String, nullable=False)
    nt_date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    nt_date_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
