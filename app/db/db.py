from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal


async def check_database() -> bool:
    """Check database connection.
    Args:
        None."""
    session = SessionLocal()
    try:
        return await check_session(session)
    finally:
        await session.close()


async def check_session(session: AsyncSession) -> bool:
    """Run database health query.
    Args:
        session (AsyncSession): Database session."""
    try:
        await session.execute(text('SELECT 1'))
        return True
    except SQLAlchemyError:
        return False
