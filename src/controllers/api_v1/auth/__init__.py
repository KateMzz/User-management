from fastapi import APIRouter

from src.controllers.api_v1.auth.ctrl_login import router as login_router
from src.controllers.api_v1.auth.ctrl_refresh_token import router as get_new_token_router
from src.controllers.api_v1.auth.ctrl_reset_pass import router as resert_pass_router
from src.controllers.api_v1.auth.ctrl_signup import router as signup_router

auth_router = APIRouter(prefix="/auth", tags=["Auth service, ver.1"])

auth_router.include_router(signup_router)
auth_router.include_router(login_router)
auth_router.include_router(get_new_token_router)
auth_router.include_router(resert_pass_router)
