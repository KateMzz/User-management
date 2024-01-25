from fastapi import HTTPException
from starlette import status

from src.models.models import User
from src.repositories.repo_user import UserRepository
from src.schemas.response import IResponse
from src.schemas.sch_user import UserCreate, UserDetail, UserDetailUpdate
from src.services.auth.auth_service import AuthService
from utils.base import AsyncBase
from utils.error_handler import UserCreateError


class UserService(AsyncBase):
    async def create_user_with_hashedpass(
        self,
        user: UserCreate,
    ):
        hashed_password = await AuthService(self.session).get_password_hash(password=user.password)
        if hashed_password:
            new_user = User(
                name=user.name,
                username=user.username,
                email=user.email,
                surname=user.surname,
                phone_number=user.phone_number,
                hashed_password=hashed_password,
                role=user.role,
                group_id=user.group_id,
            )
            create_user = await UserRepository(self.session).create_user(new_user)
            return create_user
        else:
            raise UserCreateError

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

    async def update_user(self, updated_user: UserDetailUpdate, user) -> IResponse:
        updated_user = updated_user.model_dump(exclude_none=True)
        update = await UserRepository(self.session).update_user(user_id=user.id, data=updated_user)
        updated_user_dict = await UserRepository(self.session).row_to_dict(row=update)
        return IResponse(
            payload=UserDetailUpdate(**updated_user_dict),
            status_code=200,
            message="User updated successfully",
        )

    async def user_detail(self, user):
        result = await UserRepository(self.session).row_to_dict(row=user)
        return IResponse(payload=UserDetail(**result), status_code=200, message="Success")
