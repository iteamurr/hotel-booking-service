import uuid
import sqlalchemy
import sqlalchemy.ext.asyncio as async_alchemy

import src.database.models as models
import src.schemas.hotel as hotel_schemas


async def create_hotel(
    session: async_alchemy.AsyncSession,
    description: str,
    cost: int,
) -> models.Hotel:
    session.add(new_hotel := models.Hotel(description=description, cost=cost))
    await session.flush()
    return new_hotel


async def delete_hotel(session: async_alchemy.AsyncSession, hotel_id: uuid.UUID):
    result = await session.execute(
        sqlalchemy.select(models.Hotel).where(models.Hotel.hotel_id == hotel_id)
    )
    hotel = result.scalar_one_or_none()

    if hotel:
        await session.delete(hotel)
        await session.commit()


async def get_hotels(
    session: async_alchemy.AsyncSession, order: hotel_schemas.HotelOrder
) -> list[models.Hotel]:
    order_column = getattr(models.Hotel, order.order_by)
    if order.descending:
        order_column = order_column.desc()

    result = await session.execute(
        sqlalchemy.select(models.Hotel).order_by(order_column)
    )
    return result.scalars().all()
