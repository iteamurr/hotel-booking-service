import abc

import sqlalchemy.ext.asyncio as async_alchemy

import src.infrastructure.db.repositories.booking as booking_repos
import src.infrastructure.db.repositories.hotel as hotel_repos


class AbstractUnitOfWork(abc.ABC):
    @abc.abstractmethod
    async def __aenter__(self): ...

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abc.abstractmethod
    async def commit(self): ...

    @abc.abstractmethod
    async def rollback(self): ...


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        session_factory: async_alchemy.async_sessionmaker[async_alchemy.AsyncSession],
    ):
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session: async_alchemy.AsyncSession = self._session_factory()

        self.bookings = booking_repos.BookingRepoImpl(self.session)
        self.booking_reader = booking_repos.BookingReaderImpl(self.session)

        self.hotels = hotel_repos.HotelRepoImpl(self.session)
        self.hotel_reader = hotel_repos.HotelReaderImpl(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
