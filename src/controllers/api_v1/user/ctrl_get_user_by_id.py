from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.repositories.repo_user import UserRepository
from src.schemas.response import IResponse
from src.schemas.sch_user import UserDetail
from src.services.auth.user_service import UserService
from utils.db_connection import get_async_session
from utils.error_handler import UserNotFound
from utils.permissions import RoleHandler

router = APIRouter()


@router.get(
    path="/user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=IResponse[UserDetail],
    responses={200: {"description": "Success"}, 500: {"description": "Internal server error"}},
    dependencies=[Depends(RoleHandler(role_required=["admin", "moderator"], full_access=False))],
)
async def get_user_by_id(
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
) -> IResponse:
    user = await UserRepository(session).get_user_by_id(user_id)
    if not user:
        raise UserNotFound
    result = await UserService(session).user_detail(user=user)
    return result
