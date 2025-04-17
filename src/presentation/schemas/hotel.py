import enum
import uuid

import pydantic


class HotelAddRequest(pydantic.BaseModel):
    description: str
    cost: float


class HotelAddResponse(pydantic.BaseModel):
    hotel_id: uuid.UUID


class HotelDeleteResponse(pydantic.BaseModel):
    hotel_id: uuid.UUID


class HotelListResponse(pydantic.BaseModel):
    hotel_id: uuid.UUID
    description: str
    cost: float


class HotelOrderBy(str, enum.Enum):
    cost = "cost"
    date_created = "date_created"


class HotelOrder(pydantic.BaseModel):
    order_by: HotelOrderBy = HotelOrderBy.date_created
    descending: bool = False
