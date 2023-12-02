import re
from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import EmailStr, Field, field_validator, model_validator

from settings import settings
from src.schemas.base_model import BaseORMModel
from utils.enums import UserRole


class UserDetail(BaseORMModel):
    id: UUID
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    role: UserRole
    image_path: Optional[str]
    group_id: Optional[int]


class UserDetailUpdate(BaseORMModel):
    name: Optional[str]
    surname: Optional[str]
    username: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    modified_at: datetime = Field(default=datetime.now())


class UserCreate(BaseORMModel):
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("phone_number")
    @classmethod
    def phone_validator(cls, phone_number: str):
        if not re.match(r"^(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$", phone_number):
            raise ValueError("Invalid phone number")
        return phone_number

    @model_validator(mode="after")
    def validate_passwords(cls, instance):
        if instance.password != instance.confirm_password:
            raise ValueError("Passwords do not match")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John",
                "surname": "Doe",
                "username": "johndoe",
                "phone_number": "+995555555555",
                "email": "example@gmail.com",
                "password": "secure_password",
                "confirm_password": "secure_password",
            }
        }


class LoginRequest(BaseORMModel):
    credentials: Union[str, EmailStr]
    password: str

    @staticmethod
    def categorize_field(credentials: Union[EmailStr, str]):
        if "@" in credentials and EmailStr._validate(credentials):
            return "email"
        elif re.match(r"^(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$", credentials):
            return "phone_number"
        elif isinstance(credentials, str):
            return "username"

    class Config:
        json_schema_extra = {
            "example": {
                "credentials": "johndoe" or "+995555555555" or "example@gmail.com",
                "password": "secure_password",
            }
        }


class TokenResponse(BaseORMModel):
    access_token: str
    refresh_token: str


class AccessToken(BaseORMModel):
    token: str
    expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


class RefreshToken(BaseORMModel):
    token: str
    expires_in: int = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60


class ResetPasswordRequest(BaseORMModel):
    email: EmailStr

    class Config:
        json_schema_extra = {"example": {"email": "example@gmail.com"}}
