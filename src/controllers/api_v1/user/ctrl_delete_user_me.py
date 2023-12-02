from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from src.controllers.api_v1.auth.ctrl_login import oauth2_scheme
from src.repositories.repo_user import UserRepository
from src.services.auth.user_service import UserService
from utils.db_connection import get_async_session

router = APIRouter()


@router.delete(
    path="/me",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Success"}, 500: {"description": "Internal server error"}},
)
async def delete_user(
    session: AsyncSession = Depends(get_async_session),
    token=Depends(oauth2_scheme),
):
    user = await UserService(session).get_current_user(token=token)
    await UserRepository(session).delete_user(user_id=user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "User deleted successfully"}
    )
