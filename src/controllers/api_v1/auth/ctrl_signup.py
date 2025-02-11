from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from src.schemas.response import IResponse
from src.schemas.sch_user import UserCreate
from src.services.auth.user_service import UserService
from utils.db_connection import get_async_session
from utils.error_handler import UserCreateError

router = APIRouter()


@router.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=IResponse[UserCreate],
    responses={201: {"description": "Created"}, 500: {"description": "Internal server error"}},
)
async def create_new_user(
    user: UserCreate, session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    new_user = await UserService(session).create_user_with_hashedpass(user)
    if new_user:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content={"message": "User created successfully"}
        )
    raise UserCreateError
