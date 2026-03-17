from __future__ import annotations
from uuid import uuid4
from datetime import UTC, datetime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base
from .user import User


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    images: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list
    )
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )

    author: Mapped[User] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(  # noqa: F821 # type: ignore
        back_populates="post", cascade="all, delete-orphan"
    )
    votes: Mapped[list["Vote"]] = relationship(  # noqa: F821 # type: ignore
        back_populates="post", cascade="all, delete-orphan"
    )
