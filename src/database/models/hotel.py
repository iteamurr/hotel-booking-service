import uuid
import sqlalchemy
import sqlalchemy.dialects.postgresql as psql_alchemy

import src.database.models.common as common


class Hotel(common.Base):
    __tablename__ = "hotel"

    hotel_id = sqlalchemy.Column(
        psql_alchemy.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    cost = sqlalchemy.Column(sqlalchemy.Numeric, nullable=False)
