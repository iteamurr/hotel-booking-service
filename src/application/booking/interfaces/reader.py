import abc
import uuid

import src.infrastructure.db.models.booking as booking_models


class BookingReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_hotel_id(
        self,
        hotel_id: uuid.UUID,
    ) -> list[booking_models.Booking]: ...
