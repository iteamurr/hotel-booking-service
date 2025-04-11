import uuid
import fastapi
from fastapi import status
import sqlalchemy.ext.asyncio as async_alchemy

import src.schemas.booking as booking_schemas
import src.database.dependencies as db_depends
import src.database.crud.booking as booking_crud
import src.database.crud.hotel as hotel_crud


router = fastapi.APIRouter()


@router.post(
    "/booking",
    response_model=booking_schemas.BookingAddResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Hotel with this id not found",
        },
    },
    tags=["booking"],
)
async def add_booking(
    booking: booking_schemas.BookingAddRequest,
    db: async_alchemy.AsyncSession = fastapi.Depends(db_depends.get_db),
) -> booking_schemas.BookingAddResponse:
    async with db as session:
        async with session.begin():
            hotel = await hotel_crud.get_hotel_by_id(session, booking.hotel_id)
            if not hotel:
                raise fastapi.HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Hotel with this id not found",
                )

            db_booking = await booking_crud.create_booking(
                session,
                hotel_id=booking.hotel_id,
                date_start=booking.date_start,
                date_end=booking.date_end,
            )
    return booking_schemas.BookingAddResponse(booking_id=db_booking.booking_id)


@router.delete(
    "/booking/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["booking"],
)
async def delete_booking(
    booking_id: uuid.UUID,
    db: async_alchemy.AsyncSession = fastapi.Depends(db_depends.get_db),
):
    async with db as session:
        async with session.begin():
            await booking_crud.delete_booking(session, booking_id=booking_id)


@router.get(
    "/booking/{hotel_id}/list",
    response_model=list[booking_schemas.BookingListResponse],
    status_code=status.HTTP_200_OK,
    tags=["booking"],
)
async def get_booking_list(
    hotel_id: uuid.UUID,
    db: async_alchemy.AsyncSession = fastapi.Depends(db_depends.get_db),
) -> list[booking_schemas.BookingListResponse]:
    async with db as session:
        async with session.begin():
            booking_list = await booking_crud.get_bookings_by_hotel_id(
                session=session,
                hotel_id=hotel_id,
            )
    return [
        booking_schemas.BookingListResponse(
            booking_id=booking.booking_id,
            date_start=booking.date_start,
            date_end=booking.date_end,
        )
        for booking in booking_list
    ]
