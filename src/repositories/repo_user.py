from ..models.models import User
from ..schemas.sch_user import UserCreate
from .base import AsyncBaseRepository


class UserRepository(AsyncBaseRepository):
    """
    Class contain methods for working with User table in database
    """

    async def create_user(self, user: UserCreate) -> None:
        new_user = User(**user.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
