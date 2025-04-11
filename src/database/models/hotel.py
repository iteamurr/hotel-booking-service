import datetime
import uuid

import sqlalchemy
import sqlalchemy.dialects.postgresql as pg_alchemy

import src.database.models.common as common


class Hotel(common.Base):
    __tablename__ = "hotel"

    hotel_id = sqlalchemy.Column(
        pg_alchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    cost = sqlalchemy.Column(sqlalchemy.Numeric, nullable=False)
    date_created = sqlalchemy.Column(
        sqlalchemy.DateTime,
        nullable=False,
        default=datetime.datetime.now,
    )
