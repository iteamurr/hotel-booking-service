import uuid
from datetime import date

import sqlalchemy

import src.domain.repositories.booking as booking_repos
import src.domain.repositories.common as common_repos
import src.infrastructure.db.models.booking as booking_models


class BookingRepoImpl(common_repos.SQLAlchemyRepo, booking_repos.BookingRepo):
    async def create(
        self,
        hotel_id: uuid.UUID,
        date_start: date,
        date_end: date,
    ) -> booking_models.Booking:
        booking = booking_models.Booking(
            date_start=date_start,
            date_end=date_end,
            hotel_id=hotel_id,
        )
        self.session.add(booking)
        await self.session.flush()
        return booking

    async def delete(self, booking_id: uuid.UUID):
        result = await self.session.execute(
            sqlalchemy.select(booking_models.Booking).where(
                booking_models.Booking.booking_id == booking_id
            )
        )
        booking = result.scalar_one_or_none()

        if booking:
            await self.session.delete(booking)
            await self.session.commit()


class BookingReaderImpl(common_repos.SQLAlchemyRepo, booking_repos.BookingReader):
    async def get_by_hotel_id(
        self, hotel_id: uuid.UUID
    ) -> list[booking_models.Booking]:
        result = await self.session.execute(
            sqlalchemy.select(booking_models.Booking)
            .where(booking_models.Booking.hotel_id == hotel_id)
            .order_by(booking_models.Booking.date_start.asc())
        )
        return result.scalars().all()
