from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import User
from src.repositories.repo_user import UserRepository
from src.schemas.sch_user import LoginRequest, LoginResponse
from src.services.auth.auth_utils import (
    generate_access_token,
    generate_refresh_token,
    verify_password,
)


async def check_login_creds(
    user: LoginRequest,
    session: AsyncSession,
) -> Union[LoginResponse, bool]:
    category = user.categorize_field(user.credentials)
    query_field = getattr(User, category)
    get_user_password = await UserRepository(session).check_user(user, query_field)
    if not get_user_password:
        return False
    compare_password = await verify_password(
        plain_password=user.password, hashed_password=get_user_password[0]
    )
    if not compare_password:
        return False
    access = await generate_access_token(user_cred=user.credentials)
    refresh = await generate_refresh_token(user_cred=user.credentials)
    response = LoginResponse(access_token=access.token, refresh_token=refresh.token)
    return response
