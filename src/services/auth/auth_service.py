from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from settings import settings
from src.repositories.repo_user import UserRepository
from src.schemas.sch_user import AccessToken, RefreshToken, TokenResponse
from utils.base import AsyncBase
from utils.error_handler import UserCreateError, UserNotFound


class AuthService(AsyncBase):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        if password:
            return AuthService.pwd_context.hash(password)
        else:
            raise UserCreateError

    async def generate_token(self, user_id: str, days: int) -> str:
        payload = {
            "user_id": str(user_id),
            "exp": datetime.utcnow() + timedelta(days=days),
        }

        encoded_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_token

    async def generate_access_token(self, user_id: str) -> AccessToken:
        if user_id:
            encoded_token = await self.generate_token(
                user_id, days=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            return AccessToken(token=encoded_token)
        else:
            raise UserNotFound

    async def generate_refresh_token(self, user_id: str) -> RefreshToken:
        if user_id:
            encoded_token = await self.generate_token(
                user_id, days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
            return RefreshToken(token=encoded_token)
        else:
            raise UserNotFound

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
        if refresh_token in user_tokens:
            return False
        await redis.sadd(user_id, refresh_token)
        return True
