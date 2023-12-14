from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from starlette import status

from src.controllers.api_v1 import api_v1_router
from src.controllers.api_v1.ctrl_healthcheck import router as healthcheck_router

app = FastAPI()

app.include_router(healthcheck_router)
app.include_router(api_v1_router)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": request.path_params}),
    )


@app.exception_handler(ResponseValidationError)
def validation_exception_handler_pydantic(
    request: Request, exc: ResponseValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": request.path_params}),
    )


@app.exception_handler(Exception)
def error_handler(request: Request, exc: Exception) -> JSONResponse:
    content = jsonable_encoder({"detail": "Internal server error"})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=content,
    )
