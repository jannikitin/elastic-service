from database.base import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncSession:
    session = sessionmaker()
    try:
        yield session
    finally:
        await session.close()
