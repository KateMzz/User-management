from fastapi import HTTPException
from starlette import status

from src.models.models import User
from src.repositories.repo_user import UserRepository
from src.schemas.sch_user import UserCreate
from src.services.auth.auth_service import AuthService
from utils.base import AsyncBase


class UserService(AsyncBase):
    async def create_user_with_hashedpass(
        self,
        user: UserCreate,
    ):
        hashed_password = await AuthService(self.session).get_password_hash(password=user.password)
        new_user = User(
            name=user.name,
            username=user.username,
            email=user.email,
            surname=user.surname,
            phone_number=user.phone_number,
            hashed_password=hashed_password,
            role=user.role,
        )
        create_user = await UserRepository(self.session).create_user(new_user)
        return create_user

    async def get_current_user(self, token: str):
        user_id = await AuthService(self.session).get_user_id_from_token(token=token)
        user = await UserRepository(self.session).get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
