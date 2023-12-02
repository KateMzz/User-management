from datetime import datetime, timedelta
from typing import Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from settings import settings
from src.models.models import User
from src.repositories.repo_user import UserRepository
from src.schemas.sch_user import AccessToken, LoginRequest, RefreshToken, TokenResponse
from utils.base import AsyncBase


class AuthService(AsyncBase):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

    async def authenticate(self, user: LoginRequest) -> Union[TokenResponse, bool]:
        category = user.categorize_field(user.credentials)
        query_field = getattr(User, category)
        get_user_password = await UserRepository(self.session).get_user(user, query_field)
        if not get_user_password:
            return False
        compare_password = await self.verify_password(
            plain_password=user.password, hashed_password=get_user_password[0]
        )
        if not compare_password:
            return False
        user_id = get_user_password[1]
        return await self.get_access_refresh_tokens(user_id)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return AuthService.pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(self, username: str, password: str):
        user = await UserRepository(self.session).get_user_by_username(username=username)
        if not user:
            return False
        compare_password = await self.verify_password(password, user.hashed_password)
        if not compare_password:
            return False
        return await self.get_access_refresh_tokens(user.id)

    async def get_password_hash(self, password: str) -> str:
        return AuthService.pwd_context.hash(password)

    async def generate_token(self, user_id: str, days: int) -> str:
        payload = {
            "user_id": str(user_id),
            "exp": datetime.utcnow() + timedelta(days=days),
        }

        encoded_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_token

    async def generate_access_token(self, user_id: str) -> AccessToken:
        encoded_token = await self.generate_token(
            user_id, days=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return AccessToken(token=encoded_token)

    async def generate_refresh_token(self, user_id: str) -> RefreshToken:
        encoded_token = await self.generate_token(user_id, days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        return RefreshToken(token=encoded_token)

    async def get_user_id_from_token(self, token) -> str:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id: str = payload.get("user_id")
        return user_id

    async def get_access_refresh_tokens(self, user_id: str) -> TokenResponse:
        access = await self.generate_access_token(user_id=user_id)
        refresh = await self.generate_refresh_token(user_id=user_id)
        response = TokenResponse(access_token=access.token, refresh_token=refresh.token)
        return response

    async def blacklist_token(self, refresh_token: str, redis, user_id: str) -> bool:
        user_tokens = await redis.smembers(user_id)
        if user_tokens and refresh_token in user_tokens:
            return False
        await redis.sadd(user_id, refresh_token)
        return True
