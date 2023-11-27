from fastapi import APIRouter

from src.controllers.api_v1.auth import auth_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(auth_router)
