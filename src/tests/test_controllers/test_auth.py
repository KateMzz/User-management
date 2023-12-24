import pytest
import redis.asyncio as redis
from httpx import AsyncClient
from sqlalchemy import insert, select

import main
from src.models.models import Base
from src.models.models import Group as group
from src.tests.conftest import get_test_async_session, redis_connection, test_async_engine
from utils.db_connection import connect_to_redis, get_async_session


async def test_group():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        stmt = insert(group).values(name="test_group")
        await conn.run_sync(lambda conn: conn.execute(stmt))
        query = select(group)
        result = await conn.execute(query)
        assert result.mappings().all()[0]["name"] == "test_group"


@pytest.mark.parametrize(
    "name, surname, username, phone_number, email, password, confirm_password, role, group_id",
    [
        ("test", "test", "test", "+995555555555", "test@gmail.com", "test", "test", "user", 1),
        ("admin", "admin", "admin", "+995555555551", "admin@gmail.com", "test", "test", "admin", 1),
        (
            "moderator",
            "moderator",
            "moderator",
            "+995555555557",
            "moderator@gmail.com",
            "test",
            "test",
            "moderator",
            1,
        ),
        ("user", "user", "user", "+995555555558", "user@gmail.com", "test", "test", "user", 1),
    ],
)
async def test_register(
    ac: AsyncClient,
    name,
    surname,
    username,
    phone_number,
    email,
    password,
    confirm_password,
    role,
    group_id,
):
    data = {
        "name": name,
        "surname": surname,
        "username": username,
        "phone_number": phone_number,
        "email": email,
        "password": password,
        "confirm_password": confirm_password,
        "role": role,
        "group_id": group_id,
    }

    response = await ac.post("/api/v1/auth/signup", json=data)
    assert response.status_code == 201


@pytest.mark.parametrize(
    "name, surname, username, phone_number, email, password, confirm_password, role, group_id",
    [
        ("test", "test", "test", "+995555555555", "testtest@gmail.com", "test", "test", "user", 1),
        ("test", "test", "test", "+995555555556", "test@gmail.com", "test", "test", "user", 1),
        ("test", "test", "test", "+995555555557", "test2@gmail.com", "test", "test", "user", 10),
        ("", "", "", "+995555555558", "test3@gmail.com", "test", "test", "user", 1),
    ],
)
async def test_register_fail(
    ac: AsyncClient,
    name,
    surname,
    username,
    phone_number,
    email,
    password,
    confirm_password,
    role,
    group_id,
):
    data = {
        "name": name,
        "surname": surname,
        "username": username,
        "phone_number": phone_number,
        "email": email,
        "password": password,
        "confirm_password": confirm_password,
        "role": role,
        "group_id": group_id,
    }
    response = await ac.post("/api/v1/auth/signup", json=data)
    assert response.status_code == 400


async def test_login(ac: AsyncClient):
    response = await ac.post("/api/v1/auth/login", data={"username": "test", "password": "test"})

    assert response.status_code == 200


async def test_login_fail(ac: AsyncClient):
    response = await ac.post("/api/v1/auth/login", data={"username": "test1", "password": "test"})
    assert response.status_code == 404


async def test_refresh_token_not_blacklisted(exp_token, ac: AsyncClient):
    main.app.dependency_overrides[connect_to_redis] = redis_connection
    main.app.dependency_overrides[get_async_session] = get_test_async_session
    response = await ac.post("/api/v1/auth/refresh-token", json={"token": exp_token})
    assert response.status_code == 200


async def test_refresh_token_blacklisted(exp_token, test_user_id, ac: AsyncClient):
    main.app.dependency_overrides[connect_to_redis] = redis_connection
    main.app.dependency_overrides[get_async_session] = get_test_async_session
    redis_resp = await redis.from_url("redis://localhost:6379/2?decode_responses=True")
    await redis_resp.sadd(test_user_id, exp_token)
    response = await ac.post(
        "/api/v1/auth/refresh-token",
        json={
            "token": exp_token,
        },
    )
    assert response.status_code == 403


async def test_delete_user_me(ac: AsyncClient, exp_token):
    response = await ac.delete("/api/v1/user/me", headers={"Authorization": f"Bearer {exp_token}"})
    assert response.status_code == 200
