from fastapi import FastAPI

from src.controllers.api_v1 import api_v1_router
from src.controllers.api_v1.ctrl_healthcheck import router as healthcheck_router

app = FastAPI()

app.include_router(healthcheck_router)
app.include_router(api_v1_router)
