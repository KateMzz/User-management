from fastapi import APIRouter

from src.controllers.api_v1.user.ctrl_get_user_me import router as get_user_me

user_router = APIRouter(prefix="/user", tags=["user service, ver.1"])

user_router.include_router(get_user_me)
