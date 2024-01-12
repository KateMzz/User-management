from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.controllers.api_v1.auth.ctrl_login import oauth2_scheme
from src.schemas.response import IResponse
from src.schemas.sch_user import UserDetailUpdate
from src.services.auth.user_service import UserService
from utils.db_connection import get_async_session

router = APIRouter()


@router.patch(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=IResponse[UserDetailUpdate],
    responses={200: {"description": "Success"}, 500: {"description": "Internal server error"}},
)
async def update_user_info(
    updated_user: UserDetailUpdate,
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme),
):
    user = await UserService(session).get_current_user(token=token)
    update_user = await UserService(session).update_user(updated_user=updated_user, user=user)
    return update_user
