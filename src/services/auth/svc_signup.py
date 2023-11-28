from src.models.models import User
from src.repositories.repo_user import UserRepository
from src.schemas.sch_user import UserCreate
from src.services.auth.svc_login import AuthService
from utils.base import AsyncBase


class UserService(AsyncBase):
    async def create_user_with_hashedpass(
        self,
        user: UserCreate,
    ) -> None:
        hashed_password = await AuthService(self.session).get_password_hash(password=user.password)
        new_user = User(
            name=user.name,
            username=user.username,
            email=user.email,
            surname=user.surname,
            phone_number=user.phone_number,
            hashed_password=hashed_password,
        )

        await UserRepository(self.session).create_user(new_user)
