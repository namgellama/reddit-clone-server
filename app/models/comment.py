from __future__ import annotations
from uuid import uuid4
from datetime import UTC, datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

from .post import Post
from .user import User


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(
        timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    post_id: Mapped[UUID] = mapped_column(
        ForeignKey("posts.id"), nullable=False)
    parent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("comments.id"), nullable=True)

    user: Mapped[User] = relationship(back_populates="comments")
    post: Mapped[Post] = relationship(back_populates="comments")
    upvotes: Mapped[list["Upvote"]] = relationship(
        back_populates="comment",  cascade="all, delete-orphan")

    parent: Mapped[Comment | None] = relationship(
        "Comment", remote_side=[id], back_populates="replies")
    replies: Mapped[list[Comment]] = relationship(
        "Comment", back_populates="parent",  cascade="all, delete-orphan")
