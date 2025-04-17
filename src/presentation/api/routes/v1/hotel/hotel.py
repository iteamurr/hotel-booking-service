import uuid

import fastapi
from fastapi import status

import src.domain.services.hotel as hotel_services
import src.presentation.api.routes.v1.hotel.dependencies.hotel_depends as hotel_depends
import src.presentation.schemas.hotel as hotel_schemas

router = fastapi.APIRouter()


@router.post(
    "/hotel",
    response_model=hotel_schemas.HotelAddResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["hotel"],
)
async def add_hotel(
    hotel: hotel_schemas.HotelAddRequest,
    service: hotel_services.HotelService = fastapi.Depends(
        hotel_depends.get_hotel_service
    ),
) -> hotel_schemas.HotelAddResponse:
    return await service.create_hotel(hotel)


@router.delete(
    "/hotel/{hotel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["hotel"],
)
async def delete_hotel(
    hotel_id: uuid.UUID,
    service: hotel_services.HotelService = fastapi.Depends(
        hotel_depends.get_hotel_service
    ),
):
    await service.delete_hotel(hotel_id)


@router.get(
    "/hotel/list",
    response_model=list[hotel_schemas.HotelListResponse],
    status_code=status.HTTP_200_OK,
    tags=["hotel"],
)
async def get_hotel_list(
    order: hotel_schemas.HotelOrder = fastapi.Depends(),
    service: hotel_services.HotelService = fastapi.Depends(
        hotel_depends.get_hotel_service
    ),
) -> list[hotel_schemas.HotelListResponse]:
    return await service.list_hotels(order)
