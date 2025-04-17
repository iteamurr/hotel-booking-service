import sqlalchemy.ext.asyncio as async_alchemy


class SQLAlchemyRepo:
    def __init__(self, session: async_alchemy.AsyncSession):
        self._session = session

    @property
    def session(self) -> async_alchemy.AsyncSession:
        return self._session
