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
