import asyncio
from typing import AsyncGenerator

import pytest
import redis.asyncio as redis
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import main
from main import app
from settings import settings
from src.models.models import Base
from utils.db_connection import get_async_session

test_async_engine = create_async_engine(settings.test_database_url, echo=True, future=True)


TestAsyncSessionLocal = sessionmaker(
    bind=test_async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


async def get_test_async_session() -> AsyncSession:
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_async_engine.dispose()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        yield ac


async def redis_connection():
    redis_resp = await redis.from_url("redis://localhost:6379/2?decode_responses=True")
    try:
        yield redis_resp
    finally:
        await redis_resp.flushdb()
        redis_resp.close()


main.app.dependency_overrides[get_async_session] = get_test_async_session


@pytest.fixture(autouse=True)
async def exp_token():
    exp_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiN2NhYzEyYjYtMjE5Yy00MTE3LTg4OWItYTIyYzAwYjhiODU4IiwiZXhwIjoxNzA2MDUyMzYzfQ.IM5jNPZr-5eGQI0cw3qYRHNr41jipmDxzzPG746a0xE"
    return exp_token


@pytest.fixture(autouse=True)
async def test_user_id():
    uuid = "2a6e86a9-e4d6-488d-90c1-11ea4f1f6cd7"
    return uuid
