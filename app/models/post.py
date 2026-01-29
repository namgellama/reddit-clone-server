from __future__ import annotations

from uuid import uuid4
from datetime import UTC, datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.api.v1.user.user_model import User


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC))
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True)

    author: Mapped[User] = relationship(back_populates="posts")
