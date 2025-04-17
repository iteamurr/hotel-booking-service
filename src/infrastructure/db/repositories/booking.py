import uuid
from datetime import date

import sqlalchemy

import src.application.booking.interfaces.reader as booking_reader
import src.application.booking.interfaces.repo as booking_repo
import src.infrastructure.db.models.booking as booking_models
import src.shared_kernel.building_blocks.infractructure.repo as common_repos


class BookingRepoImpl(common_repos.SQLAlchemyRepo, booking_repo.BookingRepo):
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


class BookingReaderImpl(common_repos.SQLAlchemyRepo, booking_reader.BookingReader):
    async def get_by_hotel_id(
        self, hotel_id: uuid.UUID
    ) -> list[booking_models.Booking]:
        result = await self.session.execute(
            sqlalchemy.select(booking_models.Booking)
            .where(booking_models.Booking.hotel_id == hotel_id)
            .order_by(booking_models.Booking.date_start.asc())
        )
        return result.scalars().all()
