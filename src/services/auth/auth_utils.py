from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from settings import settings
from src.schemas.sch_user import AccessToken, RefreshToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def generate_access_token(user_id: str) -> AccessToken:
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    encoded_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return AccessToken(token=encoded_token)


async def generate_refresh_token(user_id: str) -> RefreshToken:
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    }

    encoded_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return RefreshToken(token=encoded_token)
