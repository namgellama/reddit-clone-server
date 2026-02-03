from __future__ import annotations
from uuid import uuid4
from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Text, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base

from .post import Post
from .comment import Comment
from .user import User


class Upvote(Base):
    __tablename__ = "upvotes"

    __table_args__ = (
        # Only one of post_id or comment_id must be NOT NULL
        CheckConstraint(
            "(post_id IS NOT NULL AND comment_id IS NULL) OR "
            "(post_id IS NULL AND comment_id IS NOT NULL)",
            name="check_only_one_target"
        ),

        # Prevent duplicate upvotes on posts
        UniqueConstraint("user_id", "post_id", name="unique_user_post_upvote"),

        # Prevent duplicate upvotes on comments
        UniqueConstraint("user_id", "comment_id",
                         name="unique_user_comment_upvote"),
    )

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC))

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True)
    post_id: Mapped[UUID] = mapped_column(
        ForeignKey("posts.id"), nullable=True, index=True)
    comment_id: Mapped[UUID] = mapped_column(
        ForeignKey("comments.id"), nullable=True, index=True)

    user: Mapped[User] = relationship(back_populates="upvotes")
    post: Mapped[Post] = relationship(back_populates="upvotes")
    comment: Mapped[Comment] = relationship(back_populates="upvotes")
