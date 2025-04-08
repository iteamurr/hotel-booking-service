import uuid
import pydantic


class HotelAddRequest(pydantic.BaseModel):
    description: str
    cost: float


class HotelAddResponse(pydantic.BaseModel):
    hotel_id: uuid.UUID


class HotelDeleteResponse(pydantic.BaseModel):
    hotel_id: uuid.UUID
