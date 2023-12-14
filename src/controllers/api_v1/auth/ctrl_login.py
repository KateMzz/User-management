from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.controllers.api_v1.auth.auth_error_handler import UserNotFound
from src.schemas.response import IResponse
from src.schemas.sch_user import TokenResponse
from src.services.auth.auth_service import AuthService
from utils.db_connection import get_async_session

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=IResponse[TokenResponse],
    responses={200: {"description": "Success!"}, 400: {"description": "wrong credentials"}},
)
async def login(
    session: AsyncSession = Depends(get_async_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await AuthService(session).authenticate_user(form_data.username, form_data.password)
    if not user:
        raise UserNotFound
    return {"payload": user, "status_code": 200, "message": "Success"}
