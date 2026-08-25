from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey, UUID as PG_UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.core.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    jti: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    token_hash: Mapped[str] = mapped_column(String, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")

