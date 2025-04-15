import abc
import uuid

import sqlalchemy

import src.database.crud.common as crud_common
import src.database.models as models
import src.schemas.hotel as hotel_schemas


class HotelRepo(abc.ABC):
    @abc.abstractmethod
    async def create(self, description: str, cost: int) -> models.Hotel:
        pass

    @abc.abstractmethod
    async def delete(self, hotel_id: uuid.UUID) -> None:
        pass


class HotelReader(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, hotel_id: uuid.UUID) -> models.Hotel | None:
        pass

    @abc.abstractmethod
    async def get_all(self, order: hotel_schemas.HotelOrder) -> list[models.Hotel]:
        pass


class HotelRepoImpl(crud_common.SQLAlchemyRepo, HotelRepo):
    async def create(self, description: str, cost: int) -> models.Hotel:
        hotel = models.Hotel(description=description, cost=cost)
        self.session.add(hotel)
        await self.session.flush()
        return hotel

    async def delete(self, hotel_id: uuid.UUID) -> None:
        result = await self.session.execute(
            sqlalchemy.select(models.Hotel).where(models.Hotel.hotel_id == hotel_id)
        )
        hotel = result.scalar_one_or_none()
        if hotel:
            await self.session.delete(hotel)
            await self.session.commit()


class HotelReaderImpl(crud_common.SQLAlchemyRepo, HotelReader):
    async def get_by_id(self, hotel_id: uuid.UUID) -> models.Hotel | None:
        result = await self.session.execute(
            sqlalchemy.select(models.Hotel).where(models.Hotel.hotel_id == hotel_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, order: hotel_schemas.HotelOrder) -> list[models.Hotel]:
        order_column = getattr(models.Hotel, order.order_by)
        if order.descending:
            order_column = order_column.desc()

        result = await self.session.execute(
            sqlalchemy.select(models.Hotel).order_by(order_column)
        )
        return result.scalars().all()
