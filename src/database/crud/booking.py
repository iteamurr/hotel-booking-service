import uuid
import sqlalchemy
import sqlalchemy.ext.asyncio as async_alchemy

from datetime import date

import src.database.models as models


async def create_booking(
    session: async_alchemy.AsyncSession,
    hotel_id: uuid.UUID,
    date_start: date,
    date_end: date,
) -> models.Booking:
    new_booking = models.Booking(
        date_start=date_start,
        date_end=date_end,
        hotel_id=hotel_id,
    )
    session.add(new_booking)
    await session.flush()
    return new_booking


async def delete_booking(session: async_alchemy.AsyncSession, booking_id: uuid.UUID):
    result = await session.execute(
        sqlalchemy.select(models.Booking).where(models.Booking.booking_id == booking_id)
    )
    booking = result.scalar_one_or_none()

    if booking:
        await session.delete(booking)
        await session.commit()


async def get_bookings_by_hotel_id(
    session: async_alchemy.AsyncSession,
    hotel_id: uuid.UUID,
) -> list[models.Booking]:
    result = await session.execute(
        sqlalchemy.select(models.Booking)
        .where(models.Booking.hotel_id == hotel_id)
        .order_by(models.Booking.date_start.asc())
    )
    return result.scalars().all()
