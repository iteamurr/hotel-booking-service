import uuid
import fastapi
from fastapi import status
import sqlalchemy.ext.asyncio as async_alchemy

import src.schemas.hotel as hotel_schemas
import src.database.dependencies as db_depends
import src.database.crud.hotel as hotel_crud

router = fastapi.APIRouter()


@router.post(
    "/hotel",
    response_model=hotel_schemas.HotelAddResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["hotel"],
)
async def add_hotel(
    hotel: hotel_schemas.HotelAddRequest,
    db: async_alchemy.AsyncSession = fastapi.Depends(db_depends.get_db),
) -> hotel_schemas.HotelAddResponse:
    async with db as session:
        async with session.begin():
            db_hotel = await hotel_crud.create_hotel(
                session,
                description=hotel.description,
                cost=hotel.cost,
            )
            return hotel_schemas.HotelAddResponse(hotel_id=db_hotel.hotel_id)


@router.delete(
    "/hotel/{hotel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["hotel"],
)
async def delete_hotel(
    hotel_id: uuid.UUID,
    db: async_alchemy.AsyncSession = fastapi.Depends(db_depends.get_db),
):
    async with db as session:
        async with session.begin():
            await hotel_crud.delete_hotel(session, hotel_id=hotel_id)


@router.get(
    "/hotel/list",
    response_model=list[hotel_schemas.HotelListResponse],
    status_code=status.HTTP_200_OK,
    tags=["hotel"],
)
async def get_hotel_list(
    order: hotel_schemas.HotelOrder = fastapi.Depends(),
    db: async_alchemy.AsyncSession = fastapi.Depends(db_depends.get_db),
) -> list[hotel_schemas.HotelListResponse]:
    async with db as session:
        async with session.begin():
            hotel_list = await hotel_crud.get_hotels(session, order=order)
    return [
        hotel_schemas.HotelListResponse(
            hotel_id=hotel.hotel_id,
            cost=hotel.cost,
            description=hotel.description,
        )
        for hotel in hotel_list
    ]
