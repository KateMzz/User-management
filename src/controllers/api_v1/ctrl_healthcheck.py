from fastapi import APIRouter
from starlette import status

router = APIRouter()


@router.get("/healthcheck", status_code=status.HTTP_200_OK)
async def healthcheck():
    return status.HTTP_200_OK
