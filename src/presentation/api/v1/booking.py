import uuid

import fastapi
from fastapi import status

import src.domain.services.booking as booking_services
import src.presentation.api.dependencies.service as api_depends
import src.presentation.schemas.booking as booking_schemas

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
    service: booking_services.BookingService = fastapi.Depends(
        api_depends.get_booking_service
    ),
) -> booking_schemas.BookingAddResponse:
    return await service.create_booking(booking)


@router.delete(
    "/booking/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["booking"],
)
async def delete_booking(
    booking_id: uuid.UUID,
    service: booking_services.BookingService = fastapi.Depends(
        api_depends.get_booking_service
    ),
):
    await service.delete_booking(booking_id)


@router.get(
    "/booking/{hotel_id}/list",
    response_model=list[booking_schemas.BookingListResponse],
    status_code=status.HTTP_200_OK,
    tags=["booking"],
)
async def get_booking_list(
    hotel_id: uuid.UUID,
    service: booking_services.BookingService = fastapi.Depends(
        api_depends.get_booking_service
    ),
) -> list[booking_schemas.BookingListResponse]:
    return await service.list_bookings_by_hotel(hotel_id)
