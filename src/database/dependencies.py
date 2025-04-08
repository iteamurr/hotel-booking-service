import typing

import sqlalchemy.ext.asyncio as async_alchemy

import src.database.settings as settings


async def get_db() -> typing.AsyncGenerator:
    try:
        session: async_alchemy.AsyncSession = settings.async_session()
        yield session
    finally:
        await session.close()
