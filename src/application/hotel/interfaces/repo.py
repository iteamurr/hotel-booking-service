import abc
import uuid

import src.infrastructure.db.models.hotel as hotel_models


class HotelRepo(abc.ABC):
    @abc.abstractmethod
    async def create(self, description: str, cost: int) -> hotel_models.Hotel: ...

    @abc.abstractmethod
    async def delete(self, hotel_id: uuid.UUID) -> None: ...
