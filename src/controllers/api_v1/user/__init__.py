from fastapi import APIRouter

from src.controllers.api_v1.user.ctrl_delete_user_me import router as delete_user_me
from src.controllers.api_v1.user.ctrl_get_user_by_id import router as get_user_id
from src.controllers.api_v1.user.ctrl_get_user_me import router as get_user_me
from src.controllers.api_v1.user.ctrl_patch_user_by_id import router as patch_user_by_id
from src.controllers.api_v1.user.ctrl_patch_user_me import router as patch_user_me

user_router = APIRouter(prefix="/user", tags=["user service, ver.1"])

user_router.include_router(get_user_me)
user_router.include_router(patch_user_me)
user_router.include_router(delete_user_me)
user_router.include_router(get_user_id)
user_router.include_router(patch_user_by_id)
