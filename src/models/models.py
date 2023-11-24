import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

from utils.enums import UserRole

Base = declarative_base()


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    users = relationship("User", back_populates="group", lazy="selectin")


class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    phone_number = Column(String(30), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    role = Column(
        Enum(UserRole, validate_strings=True, values_callable=lambda obj: [e.value for e in obj]),
        default=UserRole.USER,
    )
    image_path = Column(String)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    modified_at = Column(
        DateTime, server_default=func.now(), onupdate=datetime.utcnow, nullable=False
    )

    group_id = Column(Integer, ForeignKey("group.id"))
    group = relationship("Group", back_populates="users", lazy="selectin")
