from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.repositories.repo_user import UserRepository
from src.schemas.response import IResponse
from src.schemas.sch_user import UserDetailUpdate
from src.services.auth.user_service import UserService
from utils.db_connection import get_async_session
from utils.error_handler import UserNotFound
from utils.permissions import RoleHandler

router = APIRouter()


@router.patch(
    path="/user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse[UserDetailUpdate],
    responses={200: {"description": "Success"}, 500: {"description": "Internal server error"}},
    dependencies=[Depends(RoleHandler(role_required=["admin"]))],
)
async def change_user_info_by_id(
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
    updated_user=Depends(UserDetailUpdate),
) -> IResponse:
    user = await UserRepository(session).get_user_by_id(user_id)
    if not user:
        raise UserNotFound
    update_user = await UserService(session).update_user(updated_user=updated_user, user=user)
    return update_user
