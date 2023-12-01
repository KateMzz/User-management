from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from src.schemas.response import IResponse
from src.schemas.sch_user import RefreshToken, TokenResponse
from src.services.auth.auth_service import AuthService
from utils.db_connection import connect_to_redis, get_async_session

router = APIRouter()


@router.post(
    path="/refresh-token",
    status_code=status.HTTP_200_OK,
    response_model=IResponse[TokenResponse],
    responses={200: {"description": "Success!"}, 400: {"description": "wrong credentials"}},
)
async def get_new_tokens(
    session: AsyncSession = Depends(get_async_session),
    refresh_token=Depends(RefreshToken),
    redis=Depends(connect_to_redis),
) -> JSONResponse:
    user_id = await AuthService(session).get_user_id_from_token(refresh_token.token)
    not_blacklisted = await AuthService(session).blacklist_token(
        redis=redis, user_id=user_id, refresh_token=refresh_token.token
    )
    if not_blacklisted:
        get_access_refresh_tokens = await AuthService(session).get_access_refresh_tokens(user_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": get_access_refresh_tokens.access_token,
                "refresh_token": get_access_refresh_tokens.refresh_token,
            },
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Refresh token is blacklisted"}
    )
