from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from settings import settings
from src.controllers.api_v1.auth.ctrl_login import oauth2_scheme
from src.schemas.sch_user import TokenData
from src.services.auth.user_service import UserService
from utils.db_connection import get_async_session

router = APIRouter()


# @router.get(
#     path="/user/{user_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=IResponse[UserDetail],
#     responses={200: {"description": "Success"}, 500: {"description": "Internal server error"}},
# )
# async def get_user_by_id(
#     token=Depends(oauth2_scheme),
#     session: AsyncSession = Depends(get_async_session),
# ) -> IResponse:
#     user = await UserService(session).get_current_user(token=token)
#     result = await UserRepository(session).row_to_dict(row=user)
#     return IResponse(payload=UserDetail(**result), status_code=200, message="Success")


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
            raise HTTPException(status_code=403, detail="Unauthorized access")


async def get_current_user_scopes(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    print(authenticate_value, "!!!!!!!")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(payload, "!!!!!!!")
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        print(token_scopes, "!!!!!!!")
        token_data = TokenData(scopes=token_scopes, username=user_id)
    except (JWTError, ValidationError):
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user_id


async def get_current_active_user(current_user=Security(get_current_user_scopes, scopes=["admin"])):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

    # if user:
    #     # Dynamically generate scopes based on user's role
    #     user_scopes = [f"{user['role'].lower()}:{user['group']}"]
    #     return user_scopes
    # else:
    #     raise HTTPException(status_code=403, detail="Invalid user")


@router.get("/user/{user_id}")
async def get_user_info(user_id: str, token: str = Depends(get_current_active_user)):
    return user_id
    # Check if the request is authorized based on roles and group membership
    # if auth_handler.is_authorized('ADMIN') or auth_handler.is_authorized('MODERATOR'):
    #     user = user_data.get(user_id)
    #     if user:
    #         return user
    #     else:
    #         raise HTTPException(status_code=404, detail="User not found")
    # else:
    #     raise HTTPException(status_code=403, detail="Unauthorized access")
