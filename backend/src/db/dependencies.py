from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncConnection
from db.engine import engine


async def get_async_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as conn:
        async with conn.begin(): 
            yield conn
