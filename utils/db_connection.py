from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

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
