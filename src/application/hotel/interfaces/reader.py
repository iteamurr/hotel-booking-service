import abc
import uuid

import src.infrastructure.db.models.hotel as hotel_models
import src.presentation.schemas.hotel as hotel_schemas


class HotelReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, hotel_id: uuid.UUID) -> hotel_models.Hotel | None: ...

    @abc.abstractmethod
    async def get_all(
        self,
        order: hotel_schemas.HotelOrder,
    ) -> list[hotel_models.Hotel]: ...
