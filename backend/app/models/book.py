from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Book(Base):
    __tablename__ = "books"

    bk_id: Mapped[int] = mapped_column(primary_key=True)
    bk_title: Mapped[str] = mapped_column(String(255), nullable=False)
    bk_author: Mapped[str] = mapped_column(String(100), nullable=False)
    bk_rating: Mapped[float] = mapped_column(Float)
