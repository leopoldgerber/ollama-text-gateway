from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine)

from app.config import DATABASE_URL


engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create database session.
    Args:
        None."""
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
