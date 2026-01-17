from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str | None] = mapped_column(
        String, nullable=True, default=None)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="author", cascade="all, delete-orphan")
