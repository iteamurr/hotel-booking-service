import abc
import uuid
from datetime import date

import sqlalchemy

import src.database.crud.common as crud_common
import src.database.models as models


class BookingRepo(abc.ABC):
    @abc.abstractmethod
    async def create(
        self, hotel_id: uuid.UUID, date_start: date, date_end: date
    ) -> models.Booking: ...

    @abc.abstractmethod
    async def delete(self, booking_id: uuid.UUID): ...


class BookingReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_hotel_id(self, hotel_id: uuid.UUID) -> list[models.Booking]: ...


class BookingRepoImpl(crud_common.SQLAlchemyRepo, BookingRepo):
    async def create(
        self,
        hotel_id: uuid.UUID,
        date_start: date,
        date_end: date,
    ) -> models.Booking:
        booking = models.Booking(
            date_start=date_start,
            date_end=date_end,
            hotel_id=hotel_id,
        )
        self.session.add(booking)
        await self.session.flush()
        return booking

    async def delete(self, booking_id: uuid.UUID):
        result = await self.session.execute(
            sqlalchemy.select(models.Booking).where(
                models.Booking.booking_id == booking_id
            )
        )
        booking = result.scalar_one_or_none()

        if booking:
            await self.session.delete(booking)
            await self.session.commit()


class BookingReaderImpl(crud_common.SQLAlchemyRepo, BookingReader):
    async def get_by_hotel_id(self, hotel_id: uuid.UUID) -> list[models.Booking]:
        result = await self.session.execute(
            sqlalchemy.select(models.Booking)
            .where(models.Booking.hotel_id == hotel_id)
            .order_by(models.Booking.date_start.asc())
        )
        return result.scalars().all()
