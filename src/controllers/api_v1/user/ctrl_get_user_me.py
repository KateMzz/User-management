from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from src.repositories.repo_user import UserRepository
from src.schemas.response import IResponse
from src.schemas.sch_user import AccessToken, UserDetail
from src.services.auth.auth_service import AuthService
from utils.db_connection import get_async_session

router = APIRouter()


@router.get(
    path="/user/me",
    status_code=status.HTTP_200_OK,
    response_model=IResponse[UserDetail],
    responses={200: {"description": "Success"}, 500: {"description": "Internal server error"}},
)
async def create_new_user(
    session: AsyncSession = Depends(get_async_session), token=Depends(AccessToken)
) -> JSONResponse:
    user_id = await AuthService(session).get_user_id_from_token(token=token.token)
    user = await UserRepository(session).get_user_info(user_id)
    result = await UserRepository(session).row_to_dict(row=user)

    # return IResponse(payload=UserDetail(**result), status_code=200, message="Success")
    return JSONResponse(content=result, status_code=200)
