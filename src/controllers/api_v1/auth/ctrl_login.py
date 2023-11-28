from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from src.schemas.response import IResponse
from src.schemas.sch_user import LoginRequest, LoginResponse
from src.services.auth.svc_login import check_login_creds
from utils.db_connection import get_async_session

router = APIRouter()


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=IResponse[LoginResponse],
    responses={200: {"description": "Success!"}, 400: {"description": "wrong credentials"}},
)
async def create_new_user(
    session: AsyncSession = Depends(get_async_session), user=Depends(LoginRequest)
) -> JSONResponse:
    user_exists = await check_login_creds(user, session)
    if not user_exists:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User not found"}
        )
    access_token = user_exists.access_token
    refresh_token = user_exists.refresh_token

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": access_token, "refresh_token": refresh_token},
    )
