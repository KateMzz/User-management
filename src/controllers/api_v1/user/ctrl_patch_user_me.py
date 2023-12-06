from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.controllers.api_v1.auth.ctrl_login import oauth2_scheme
from src.repositories.repo_user import UserRepository
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
    session: AsyncSession = Depends(get_async_session),
    token=Depends(oauth2_scheme),
    updated_user=Depends(UserDetailUpdate),
):
    user = await UserService(session).get_current_user(token=token)
    updated_user = updated_user.model_dump()
    update = await UserRepository(session).update_user(user_id=user.id, data=updated_user)
    updated_user_dict = await UserRepository(session).row_to_dict(row=update)
    return IResponse(
        payload=UserDetailUpdate(**updated_user_dict),
        status_code=200,
        message="User updated successfully",
    )
