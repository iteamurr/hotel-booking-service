import uuid
import pydantic
from datetime import datetime, date


class BookingAddRequest(pydantic.BaseModel):
    hotel_id: uuid.UUID
    date_start: date
    date_end: date

    @pydantic.field_validator("date_start", "date_end", mode="before")
    @classmethod
    def validate_date_format(cls, v):
        if isinstance(v, date):
            return v
        try:
            return datetime.strptime(v, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            raise ValueError("Date must be in format 'YYYY-MM-DD'")


class BookingAddResponse(pydantic.BaseModel):
    booking_id: uuid.UUID


class BookingListResponse(pydantic.BaseModel):
    booking_id: uuid.UUID
    date_start: date
    date_end: date
