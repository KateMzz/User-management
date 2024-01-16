from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.api_v1.auth.ctrl_login import oauth2_scheme
from src.models.models import User
from src.services.auth.user_service import UserService
from utils.db_connection import get_async_session


class RoleHandler:
    def __init__(self, role_required, full_access=True):
        self.role_required = role_required
        self.full_access = full_access

    async def __call__(
        self,
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session),
    ):
        user = await UserService(session).get_current_user(token=token)
        role = user.role.value

        user_info = select(
            User.id,
            User.surname,
            User.name,
            User.username,
            User.email,
            User.phone_number,
            User.group_id,
            User.image_path,
            User.role,
        )
        if role == "admin":
            return user_info
        if role in self.role_required:
            if self.full_access:
                return user_info
            return user_info.filter(User.group_id == user.group_id)
        else:
            raise HTTPException(status_code=403, detail="Not enough permissions")
