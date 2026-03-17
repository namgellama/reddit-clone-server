from uuid import uuid4
import enum
from datetime import UTC, datetime
from sqlalchemy import DateTime, Enum, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base

from .post import Post
from .comment import Comment
from .user import User


class VoteType(str, enum.Enum):
    UPVOTE = "UPVOTE"
    DOWNVOTE = "DOWNVOTE"


class Vote(Base):
    __tablename__ = "votes"

    __table_args__ = (
        # Only one of post_id or comment_id must be NOT NULL
        CheckConstraint(
            "(post_id IS NOT NULL AND comment_id IS NULL) OR "
            "(post_id IS NULL AND comment_id IS NOT NULL)",
            name="check_only_one_target",
        ),
        # Prevent duplicate votes on posts
        UniqueConstraint("user_id", "post_id", name="unique_user_post_vote"),
        # Prevent duplicate votes on comments
        UniqueConstraint("user_id", "comment_id", name="unique_user_comment_vote"),
    )

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    type: Mapped[VoteType] = mapped_column(Enum(VoteType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    post_id: Mapped[UUID] = mapped_column(
        ForeignKey("posts.id"), nullable=True, index=True
    )
    comment_id: Mapped[UUID] = mapped_column(
        ForeignKey("comments.id"), nullable=True, index=True
    )

    user: Mapped[User] = relationship(back_populates="votes")
    post: Mapped[Post] = relationship(back_populates="votes")
    comment: Mapped[Comment] = relationship(back_populates="votes")
