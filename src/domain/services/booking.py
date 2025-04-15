import uuid

import fastapi

import src.infrastructure.db.repositories.uow as repos_uow
import src.presentation.schemas.booking as booking_schemas


class BookingService:
    def __init__(self, uow: repos_uow.SQLAlchemyUnitOfWork):
        self.uow = uow

    async def create_booking(
        self,
        booking_data: booking_schemas.BookingAddRequest,
    ) -> booking_schemas.BookingAddResponse:
        async with self.uow:
            hotel = await self.uow.hotel_reader.get_by_id(booking_data.hotel_id)
            if not hotel:
                raise fastapi.HTTPException(
                    status_code=fastapi.status.HTTP_404_NOT_FOUND,
                    detail="Hotel with this id not found",
                )

            booking = await self.uow.bookings.create(
                hotel_id=booking_data.hotel_id,
                date_start=booking_data.date_start,
                date_end=booking_data.date_end,
            )

            return booking_schemas.BookingAddResponse(booking_id=booking.booking_id)

    async def delete_booking(self, booking_id: uuid.UUID):
        async with self.uow:
            await self.uow.bookings.delete(booking_id)

    async def list_bookings_by_hotel(
        self,
        hotel_id: uuid.UUID,
    ) -> list[booking_schemas.BookingListResponse]:
        async with self.uow:
            bookings = await self.uow.booking_reader.get_by_hotel_id(hotel_id)
            return [
                booking_schemas.BookingListResponse(
                    booking_id=b.booking_id,
                    date_start=b.date_start,
                    date_end=b.date_end,
                )
                for b in bookings
            ]
