import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from utils.enums import UserRole


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    users: Mapped[list] = relationship("User", back_populates="group")


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, validate_strings=True, values_callable=lambda obj: [e.value for e in obj]),
        default=UserRole.USER,
    )
    image_path: Mapped[str] = mapped_column(nullable=True)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    modified_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=datetime.utcnow, nullable=False
    )

    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), nullable=True, default=None)
    group: Mapped[Group] = relationship("Group", back_populates="users")
