from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import asc, desc, or_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.models.models import User
from src.schemas.response import IResponse
from src.schemas.sch_user import Users
from utils.db_connection import get_async_session
from utils.permissions import RoleHandler

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Success"}, 500: {"description": "Internal server error"}},
)
async def get_filtered_users(
    session: AsyncSession = Depends(get_async_session),
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1, le=100),
    filter_by_name: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    order_by: Optional[str] = Query("asc"),
    query=Depends(RoleHandler(role_required=["admin", "moderator"], full_access=False)),
) -> IResponse:
    if filter_by_name:
        query = query.filter(
            or_(User.name.ilike(f"%{filter_by_name}%"), User.surname.ilike(f"%{filter_by_name}%"))
        )
    if sort_by and order_by:
        order = (
            asc(getattr(User, sort_by))
            if order_by.lower() == "asc"
            else desc(getattr(User, sort_by))
        )
        query = query.order_by(order)
    result = await session.execute(query.offset((page - 1) * limit).limit(limit))
    users = result.mappings().all()
    payload = {"users": []}
    for user in users:
        user = Users(**user)
        payload["users"].append(user)
    return IResponse(payload=payload, status_code=200, message="Success")
