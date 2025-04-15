import sqlalchemy.ext.asyncio as async_alchemy

import src.database.crud.booking as crud_booking
import src.database.crud.common as crud_common
import src.database.crud.hotel as crud_hotel


class SQLAlchemyUnitOfWork(crud_common.AbstractUnitOfWork):
    def __init__(
        self,
        session_factory: async_alchemy.async_sessionmaker[async_alchemy.AsyncSession],
    ):
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session: async_alchemy.AsyncSession = self._session_factory()

        self.bookings = crud_booking.BookingRepoImpl(self.session)
        self.booking_reader = crud_booking.BookingReaderImpl(self.session)

        self.hotels = crud_hotel.HotelRepoImpl(self.session)
        self.hotel_reader = crud_hotel.HotelReaderImpl(self.session)

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
