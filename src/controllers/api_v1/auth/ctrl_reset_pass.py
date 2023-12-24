from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from src.repositories.repo_user import UserRepository
from src.schemas.sch_user import ResetPasswordRequest
from utils.db_connection import get_async_session

router = APIRouter()


@router.post(
    path="/reset-password",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Success!"}, 400: {"description": "wrong email"}},
)
async def reset_password(
    input: ResetPasswordRequest, session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    user = await UserRepository(session).get_user_by_email(input.email)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Wrong email"}
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Success!"})
