import pytest
import redis.asyncio as redis
from httpx import AsyncClient
from sqlalchemy import select

from settings import settings
from src.models.models import Group

ENDPOINT = "/api/v1/auth"


async def test_group_factory(async_test_session, create_group):
    query = select(Group).where(Group.id == create_group.id)
    result = await async_test_session.execute(query)
    saved_group = result.scalar()
    assert saved_group is not None
    assert saved_group.name == create_group.name
    assert saved_group.id == create_group.id


@pytest.mark.parametrize(
    "name, surname, username, phone_number, email, password, confirm_password, role",
    [
        ("test1", "test1", "test1", "+995555555555", "test1@gmail.com", "test", "test", "user"),
        ("admin", "admin", "admin", "+995555555551", "admin@gmail.com", "test", "test", "admin"),
        (
            "moderator",
            "moderator",
            "moderator",
            "+995555555557",
            "moderator@gmail.com",
            "test",
            "test",
            "moderator",
        ),
        ("user", "user", "user", "+995555555558", "user@gmail.com", "test", "test", "user"),
    ],
)
async def test_register(
    ac: AsyncClient, name, surname, username, phone_number, email, password, confirm_password, role
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
    }

    response = await ac.post(f"{ENDPOINT}/signup", json=data)
    assert response.status_code == 201
    assert "User created successfully" in response.text


@pytest.mark.parametrize(
    "name, surname, username, phone_number, email, password, confirm_password, role, result",
    [
        (
            "test1",
            "test1",
            "test1",
            "+995555555555",
            "testtest@gmail.com",
            "test",
            "test",
            "user",
            "(username)=(test1)",
        ),
        (
            "test",
            "test",
            "test",
            "+995555555556",
            "test1@gmail.com",
            "test",
            "test",
            "user",
            "(email)=(test1@gmail.com)",
        ),
        (
            "",
            "",
            "",
            "+995555555558",
            "test3@gmail.com",
            "test",
            "test",
            "user",
            "(phone_number)=(+995555555558)",
        ),
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
    result,
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
    }
    response = await ac.post(f"{ENDPOINT}/signup", json=data)
    assert response.status_code == 400
    assert result in response.text


async def test_login(async_test_session, ac: AsyncClient, create_user):
    user = await create_user()
    response = await ac.post(
        f"{ENDPOINT}/login", data={"username": user.username, "password": "test"}
    )
    assert response.status_code == 200
    assert "access_token" in response.text


async def test_login_fail(ac: AsyncClient):
    response = await ac.post(f"{ENDPOINT}/login", data={"username": "test4", "password": "test"})
    assert response.status_code == 404
    assert "Resource not found" in response.text


async def test_refresh_token_not_blacklisted(exp_token, ac: AsyncClient):
    response = await ac.post(f"{ENDPOINT}/refresh-token", json={"token": exp_token})
    assert response.status_code == 200
    assert "access_token" and "refresh_token" in response.text


async def test_refresh_token_blacklisted(exp_token, test_user_id, ac: AsyncClient):
    redis_resp = await redis.from_url(settings.TEST_REDIS_URL)
    await redis_resp.sadd(test_user_id, exp_token)
    response = await ac.post(
        "/api/v1/auth/refresh-token",
        json={
            "token": exp_token,
        },
    )
    assert response.status_code == 403
    assert "Token is blacklisted" in response.text
