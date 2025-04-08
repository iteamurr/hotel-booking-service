import sqlalchemy.ext.asyncio as async_alchemy


import src.database.models as models


async def create_hotel(
    session: async_alchemy.AsyncSession,
    description: str,
    cost: int,
) -> models.Hotel:
    session.add(new_hotel := models.Hotel(description=description, cost=cost))
    await session.flush()
    return new_hotel
