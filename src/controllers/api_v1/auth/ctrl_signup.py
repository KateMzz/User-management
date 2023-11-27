from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from src.repositories.repo_user import UserRepository
from src.schemas.response import IResponse
from src.schemas.sch_user import UserCreate
from utils.db_connection import get_async_session

router = APIRouter()


fields = {
    "name": "name",
    "surname": "surname",
    "username": "username",
    "phone_number": "phone_number",
    "email": "hey@gmail.com",
    "hashed_password": "hashed_password",
}


@router.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=IResponse[UserCreate],
    responses={201: {"description": "Created"}, 500: {"description": "Internal server error"}},
)
async def create_new_user(
    session: AsyncSession = Depends(get_async_session), user=Depends(UserCreate)
):
    await UserRepository(session).create_user(user=user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"message": "User created successfully"}
    )
