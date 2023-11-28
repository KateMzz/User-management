from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from src.schemas.sch_user import UserCreate
from utils.db_connection import get_async_session

router = APIRouter()


@router.post(
    path="/signup",
    status_code=status.HTTP_200_OK,
    # response_model=IResponse[UserCreate],
    responses={200: {"description": "Created"}, 500: {"description": "Internal server error"}},
)
async def get_new_tokens(
    session: AsyncSession = Depends(get_async_session), user=Depends(UserCreate)
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "success", "message": "User created successfully"},
    )
