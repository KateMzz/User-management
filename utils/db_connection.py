import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from settings import settings

async_engine = create_async_engine(settings.database_url, echo=True, future=True)


AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def connect_to_redis():
    redis_connection = await redis.from_url(settings.REDIS_URL)
    try:
        yield redis_connection
    finally:
        await redis_connection.close()


test_async_engine = create_async_engine(settings.test_database_url, echo=True, future=True)


TestAsyncSessionLocal = scoped_session(
    sessionmaker(
        bind=test_async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
    )
)


async def get_test_async_session() -> AsyncSession:
    async with TestAsyncSessionLocal() as session:
        yield session
