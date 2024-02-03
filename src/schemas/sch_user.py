import re
from datetime import datetime
from typing import Optional, Union

from pydantic import EmailStr, Field, field_validator, model_validator

from settings import settings
from src.schemas.base_model import BaseORMModel
from utils.enums import UserRole


class UserDetail(BaseORMModel):
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    role: UserRole = Field(default=UserRole.USER)
    image_path: Optional[str] = Field(default=None)
    group_id: Optional[int] = Field(default=None)


class UserDetailUpdate(BaseORMModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    image_path: Optional[str] = Field(default=None)
    modified_at: datetime = Field(default=datetime.now())


class UserCreate(BaseORMModel):
    name: str
    surname: str
    username: str
    phone_number: str
    email: EmailStr
    password: str
    confirm_password: str
    role: UserRole = Field(default=UserRole.USER)
    group_id: Optional[int] = None
    image_path: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def phone_validator(cls, phone_number: str):
        if not re.match(r"^(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$", phone_number):
            raise ValueError("Invalid phone number")
        return phone_number

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


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

    class ConfigDict:
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

    class ConfigDict:
        json_schema_extra = {"example": {"email": "example@gmail.com"}}


class Users(BaseORMModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    image_path: Optional[str] = None
    group_id: Optional[int] = None
