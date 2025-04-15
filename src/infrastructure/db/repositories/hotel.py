import uuid

import sqlalchemy

import src.domain.repositories.common as common_repos
import src.domain.repositories.hotel as hotel_repos
import src.infrastructure.db.models.hotel as hotel_models
import src.presentation.schemas.hotel as hotel_schemas


class HotelRepoImpl(common_repos.SQLAlchemyRepo, hotel_repos.HotelRepo):
    async def create(self, description: str, cost: int) -> hotel_models.Hotel:
        hotel = hotel_models.Hotel(description=description, cost=cost)
        self.session.add(hotel)
        await self.session.flush()
        return hotel

    async def delete(self, hotel_id: uuid.UUID) -> None:
        result = await self.session.execute(
            sqlalchemy.select(hotel_models.Hotel).where(
                hotel_models.Hotel.hotel_id == hotel_id
            )
        )
        hotel = result.scalar_one_or_none()
        if hotel:
            await self.session.delete(hotel)
            await self.session.commit()


class HotelReaderImpl(common_repos.SQLAlchemyRepo, hotel_repos.HotelReader):
    async def get_by_id(self, hotel_id: uuid.UUID) -> hotel_models.Hotel | None:
        result = await self.session.execute(
            sqlalchemy.select(hotel_models.Hotel).where(
                hotel_models.Hotel.hotel_id == hotel_id
            )
        )
        return result.scalar_one_or_none()

    async def get_all(
        self, order: hotel_schemas.HotelOrder
    ) -> list[hotel_models.Hotel]:
        order_column = getattr(hotel_models.Hotel, order.order_by)
        if order.descending:
            order_column = order_column.desc()

        result = await self.session.execute(
            sqlalchemy.select(hotel_models.Hotel).order_by(order_column)
        )
        return result.scalars().all()
