from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.controllers.api_v1.auth.ctrl_login import oauth2_scheme
from src.repositories.repo_user import UserRepository
from src.schemas.response import IResponse
from src.schemas.sch_user import UserDetail
from src.services.auth.user_service import UserService
from utils.db_connection import get_async_session

router = APIRouter()


@router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=IResponse[UserDetail],
    responses={200: {"description": "Success"}, 500: {"description": "Internal server error"}},
)
async def get_user_info(
    token=Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> IResponse:
    user = await UserService(session).get_current_user(token=token)
    result = await UserRepository(session).row_to_dict(row=user)
    return IResponse(payload=UserDetail(**result), status_code=200, message="Success")
