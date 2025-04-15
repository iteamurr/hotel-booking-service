import abc
import uuid
from datetime import date

import src.infrastructure.db.models.booking as booking_models


class BookingRepo(abc.ABC):
    @abc.abstractmethod
    async def create(
        self, hotel_id: uuid.UUID, date_start: date, date_end: date
    ) -> booking_models.Booking: ...

    @abc.abstractmethod
    async def delete(self, booking_id: uuid.UUID): ...


class BookingReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_hotel_id(
        self, hotel_id: uuid.UUID
    ) -> list[booking_models.Booking]: ...
