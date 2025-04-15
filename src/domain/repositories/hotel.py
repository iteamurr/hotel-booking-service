import abc
import uuid

import src.infrastructure.db.models.hotel as hotel_models
import src.presentation.schemas.hotel as hotel_schemas


class HotelRepo(abc.ABC):
    @abc.abstractmethod
    async def create(self, description: str, cost: int) -> hotel_models.Hotel:
        pass

    @abc.abstractmethod
    async def delete(self, hotel_id: uuid.UUID) -> None:
        pass


class HotelReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, hotel_id: uuid.UUID) -> hotel_models.Hotel | None:
        pass

    @abc.abstractmethod
    async def get_all(
        self, order: hotel_schemas.HotelOrder
    ) -> list[hotel_models.Hotel]:
        pass
