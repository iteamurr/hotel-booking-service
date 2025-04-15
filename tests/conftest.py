import datetime
import os
import random
import types
import typing
import uuid

import alembic.command as alembic_command
import httpx
import pytest
import sqlalchemy.ext.asyncio as async_alchemy
import sqlalchemy.orm as orm_alchemy
import sqlalchemy_utils
from alembic.config import Config

import src.__main__ as src_main
import src.api.dependencies.session as db_depends
import src.config as src_config
import src.database.models as src_models
import tests.utils as tests_utils


@pytest.fixture()
def postgres() -> typing.Generator[str, None, None]:
    """
    Creates a temporary PostgreSQL database for testing and drops it after tests are done.
    """
    src_config.get_db_settings.cache_clear()  # To clear "POSTGRES_DB" value

    os.environ["POSTGRES_DB"] = "-".join([uuid.uuid4().hex, "pytest"])

    tmp_url = src_config.get_db_url_sync()
    if not sqlalchemy_utils.database_exists(tmp_url):
        sqlalchemy_utils.create_database(tmp_url)

    try:
        yield src_config.get_db_url()
    finally:
        sqlalchemy_utils.drop_database(tmp_url)


def run_upgrade(connection, cfg):
    """
    Runs Alembic migrations using a given connection and Alembic config.
    """
    cfg.attributes["connection"] = connection
    alembic_command.upgrade(cfg, "head")


async def run_async_upgrade(config: Config, database_uri: str):
    """
    Runs Alembic migrations asynchronously using the provided database URI.
    """
    async_engine = async_alchemy.create_async_engine(database_uri, echo=True)
    async with async_engine.begin() as conn:
        await conn.run_sync(run_upgrade, config)


@pytest.fixture
def alembic_config(postgres) -> Config:
    """
    Returns a configured Alembic Config object for database migration.
    """
    cmd_options = types.SimpleNamespace(
        config="src/database/",
        name="alembic",
        pg_url=postgres,
        raiseerr=False,
        x=None,
    )
    return tests_utils.make_alembic_config(cmd_options)


@pytest.fixture
def alembic_engine():
    """
    Provides an async SQLAlchemy engine using the test database URL.
    """
    return async_alchemy.create_async_engine(src_config.get_db_url_sync(), echo=True)


@pytest.fixture
async def migrated_postgres(postgres, alembic_config: Config):
    """
    Applies Alembic migrations to the test PostgreSQL database before tests run.
    """
    await run_async_upgrade(alembic_config, postgres)


@pytest.fixture
async def client(
    migrated_postgres,
    manager: db_depends.SessionManager = db_depends.SessionManager(),
) -> typing.AsyncGenerator[httpx.AsyncClient, None]:
    """
    Returns an HTTPX async client with an ASGI app, ready for API testing.
    """
    app = src_main.get_app()
    manager.refresh()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def engine_async(
    postgres,
) -> typing.AsyncGenerator[async_alchemy.AsyncEngine, None]:
    """
    Creates and yields an async SQLAlchemy engine connected to the test database.
    """
    engine = async_alchemy.create_async_engine(postgres, future=True)
    yield engine
    await engine.dispose()


@pytest.fixture
def session_factory_async(engine_async) -> orm_alchemy.sessionmaker:
    """
    Provides a SQLAlchemy async session factory bound to the test engine.
    """
    return orm_alchemy.sessionmaker(
        engine_async,
        class_=async_alchemy.AsyncSession,
        expire_on_commit=False,
    )


@pytest.fixture
async def session(
    session_factory_async,
) -> typing.AsyncGenerator[async_alchemy.AsyncSession, None]:
    """
    Yields an active SQLAlchemy async session for database interaction in tests.
    """
    async with session_factory_async() as session:
        yield session


@pytest.fixture
async def hotel(session) -> src_models.Hotel:
    test_hotel = src_models.Hotel(
        description="Test Hotel",
        cost=150,
    )
    session.add(test_hotel)
    await session.commit()
    await session.refresh(test_hotel)
    return test_hotel


@pytest.fixture
async def hotel_factory(
    session: async_alchemy.AsyncSession,
) -> tests_utils.HotelFactory:
    class Factory:
        async def make_hotel(self) -> src_models.Hotel:
            test_hotel = src_models.Hotel(
                description=f"Test Hotel {uuid.uuid4()}",
                cost=random.randint(50, 500),
            )
            session.add(test_hotel)
            await session.commit()
            await session.refresh(test_hotel)

            return test_hotel

    return Factory()


@pytest.fixture
async def booking_factory(
    session: async_alchemy.AsyncSession,
    hotel: src_models.Hotel,
) -> tests_utils.HotelBookingFactory:
    class Factory:
        def __init__(self):
            self._hotel_id = hotel.hotel_id

        @property
        def hotel_id(self):
            return self._hotel_id

        @hotel_id.setter
        def hotel_id(self, value: uuid.UUID):
            self._hotel_id = value

        async def make_booking(self) -> src_models.Booking:
            date_start = datetime.date(2025, 1, 1) + datetime.timedelta(
                days=random.randint(0, 365)
            )
            test_booking = src_models.Booking(
                date_start=date_start,
                date_end=date_start + datetime.timedelta(days=random.randint(1, 14)),
                hotel_id=hotel.hotel_id,
            )
            session.add(test_booking)
            await session.commit()
            await session.refresh(test_booking)

            return test_booking

    return Factory()
