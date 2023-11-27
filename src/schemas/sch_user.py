from datetime import date
from uuid import UUID

from pydantic import EmailStr

from utils.enums import UserRole

from .base_model import BaseORMModel


class UserDetail(BaseORMModel):
    id: UUID
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    role: UserRole
    image_path: str
    is_blocked: bool
    created_at: date
    modified_at: date
    group: str


class UserCreate(BaseORMModel):
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    hashed_password: str
