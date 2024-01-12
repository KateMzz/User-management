import asyncio
from typing import AsyncGenerator

import pytest
import redis.asyncio as redis
from httpx import AsyncClient
from pytest_factoryboy import register
from sqlalchemy.ext.asyncio import AsyncSession

import main
from main import app
from settings import settings
from src.models.models import Base
from src.tests.factories import GroupFactory, UserFactory
from utils.db_connection import (
    TestAsyncSessionLocal,
    connect_to_redis,
    get_async_session,
    get_test_async_session,
    test_async_engine,
)

register(GroupFactory)
register(UserFactory)


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with test_async_engine.begin() as conn:
        assert settings.TEST_DB_NAME == "test_user_manager"
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_async_engine.dispose()


@pytest.fixture(name="async_test_session", scope="function")
async def create_async_test_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create async session at the start of the test and close it
    at the end.
    """
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        yield ac


async def test_redis_connection():
    redis_resp = await redis.from_url("redis://localhost:6379/2?decode_responses=True")
    try:
        yield redis_resp
    finally:
        await redis_resp.flushdb()
        redis_resp.close()


main.app.dependency_overrides[get_async_session] = get_test_async_session


@pytest.fixture(autouse=True)
async def exp_token():
    exp_token = settings.TOKEN
    return exp_token


@pytest.fixture(autouse=True)
async def test_user_id():
    uuid = settings.USER_ID
    return uuid


@pytest.fixture
async def get_token(request, ac: AsyncClient, create_user):
    try:
        kwargs = request.param
    except AttributeError:
        kwargs = {}
    finally:
        user = await create_user(**kwargs)
        response = await ac.post(
            "/api/v1/auth/login", data={"username": user.username, "password": "test"}
        )
        assert response.status_code == 200
        return response.json()["access_token"]


@pytest.fixture
async def create_user(async_test_session):
    async def _create_user(**kwargs):
        user_instance = UserFactory(**kwargs)
        async_test_session.add(user_instance)
        await async_test_session.commit()
        return user_instance

    return _create_user


@pytest.fixture
async def create_group(async_test_session):
    new_group = GroupFactory()
    async_test_session.add(new_group)
    await async_test_session.commit()
    return new_group


main.app.dependency_overrides[connect_to_redis] = test_redis_connection


@pytest.fixture(scope="function", autouse=True)
def reset_factory_boy_sequences() -> None:
    for factor in (GroupFactory, UserFactory):
        factor.reset_sequence()
