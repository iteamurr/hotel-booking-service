import os
import types
import typing
import uuid

from alembic.config import Config

import src.database.models as src_models


class HotelBookingFactory(typing.Protocol):
    def make_booking(self) -> typing.Awaitable[src_models.Booking]: ...
    @property
    def hotel_id(self) -> uuid.UUID: ...


class HotelFactory(typing.Protocol):
    def make_hotel(self) -> typing.Awaitable[src_models.Hotel]: ...


def make_alembic_config(cmd_options: types.SimpleNamespace) -> Config:
    """
    Creates and returns a fully configured Alembic Config object.
    """
    alembic_ini_path = os.path.join(cmd_options.config, "alembic.ini")

    config = Config(
        file_=alembic_ini_path,
        ini_section=cmd_options.name,
        cmd_opts=cmd_options,
    )
    alembic_script_location = os.path.join(
        cmd_options.config,
        config.get_main_option("script_location"),
    )

    config.set_main_option("script_location", alembic_script_location)
    config.set_main_option("sqlalchemy.url", cmd_options.pg_url)
    return config
