from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import User
from src.repositories.repo_user import UserRepository
from src.schemas.sch_user import UserCreate
from src.services.auth.auth_utils import get_password_hash


async def create_user_with_hashedpass(
    user: UserCreate,
    session: AsyncSession,
) -> None:
    hashed_password = await get_password_hash(password=user.password)
    new_user = User(
        name=user.name,
        username=user.username,
        email=user.email,
        surname=user.surname,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
    )

    await UserRepository(session).create_user(new_user)
