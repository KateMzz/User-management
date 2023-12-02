from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import class_mapper

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

    async def get_user_by_email(self, email) -> Optional[str]:
        query = select(User.email).filter(User.email == email)
        result = (await self.session.execute(query)).one_or_none()
        return result

    async def get_user_by_username(self, username) -> Optional[str]:
        query = select(User).filter(User.username == username)
        result = (await self.session.execute(query)).scalar_one_or_none()
        return result

    async def row_to_dict(self, row) -> dict:
        result = {}

        for column in class_mapper(row.__class__).mapped_table.columns:
            value = getattr(row, column.name)

            if isinstance(value, Enum):
                result[column.name] = value.value
            elif isinstance(value, UUID):
                result[column.name] = str(value)
            elif isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value

        return result

    async def get_user_by_id(self, user_id) -> Optional[str]:
        query = select(User).filter(User.id == user_id)
        result = (await self.session.execute(query)).scalar_one_or_none()
        return result

    async def update_user(self, user_id, data):
        query = update(User).where(User.id == user_id).values(**data)
        await self.session.execute(query)
        await self.session.commit()
        res = await self.get_user_by_id(user_id)
        return res

    async def delete_user(self, user_id):
        user = await self.session.get(User, user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
