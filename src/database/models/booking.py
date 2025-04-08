import uuid
import sqlalchemy
import sqlalchemy.orm as orm_alchemy
import sqlalchemy.dialects.postgresql as pg_alchemy

import src.database.models.common as common


class Booking(common.Base):
    __tablename__ = "booking"

    booking_id = sqlalchemy.Column(
        pg_alchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    date_start = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    date_end = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    hotel_id: orm_alchemy.Mapped[uuid.UUID] = orm_alchemy.mapped_column(
        pg_alchemy.UUID(as_uuid=True),
        sqlalchemy.ForeignKey("hotel.hotel_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
