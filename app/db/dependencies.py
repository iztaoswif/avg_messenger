from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.engine import async_session


async def get_asyncsession() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
