from typing import Optional

from sqlalchemy import select

from utils.base import AsyncBase

from ..models.models import User


class UserRepository(AsyncBase):
    """
    Class contains methods for working with User table in database
    """

    async def create_user(self, fields) -> None:
        self.session.add(fields)
        await self.session.commit()
        await self.session.refresh(fields)

    async def get_user(self, user, query_field) -> Optional[str]:
        query = select(User.hashed_password, User.id).filter(query_field == user.credentials)
        result = (await self.session.execute(query)).one_or_none()
        return result
