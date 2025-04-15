import uuid

import src.database.crud.uow as crud_uow
import src.schemas.hotel as hotel_schemas


class HotelService:
    def __init__(self, uow: crud_uow.SQLAlchemyUnitOfWork):
        self.uow = uow

    async def create_hotel(
        self,
        data: hotel_schemas.HotelAddRequest,
    ) -> hotel_schemas.HotelAddResponse:
        async with self.uow:
            hotel = await self.uow.hotels.create(
                description=data.description, cost=data.cost
            )
            return hotel_schemas.HotelAddResponse(hotel_id=hotel.hotel_id)

    async def delete_hotel(self, hotel_id: uuid.UUID):
        async with self.uow:
            await self.uow.hotels.delete(hotel_id)

    async def list_hotels(
        self,
        order: hotel_schemas.HotelOrder,
    ) -> list[hotel_schemas.HotelListResponse]:
        async with self.uow:
            hotels = await self.uow.hotel_reader.get_all(order=order)
            return [
                hotel_schemas.HotelListResponse(
                    hotel_id=h.hotel_id, cost=h.cost, description=h.description
                )
                for h in hotels
            ]
