from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.api_v1.auth.ctrl_login import oauth2_scheme
from src.services.auth.user_service import UserService
from utils.db_connection import get_async_session


class RoleHandler:
    def __init__(self, role_required):
        self.role_required = role_required

    async def __call__(
        self,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session),
    ):
        user = await UserService(session).get_current_user(token=token)
        if user.role.value in self.role_required:
            return user
        else:
            raise HTTPException(status_code=403, detail="Not enough permissions")
