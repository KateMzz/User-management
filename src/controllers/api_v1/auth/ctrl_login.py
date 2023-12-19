from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.services.auth.auth_service import AuthService
from utils.db_connection import get_async_session
from utils.error_handler import UserNotFound

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Success!"}, 400: {"description": "wrong credentials"}},
)
async def login(
    session: AsyncSession = Depends(get_async_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await AuthService(session).authenticate_user(form_data.username, form_data.password)
    if not user:
        raise UserNotFound
    return {
        "access_token": user.access_token,
        "refresh_token": user.refresh_token,
        "token_type": "Bearer",
    }
