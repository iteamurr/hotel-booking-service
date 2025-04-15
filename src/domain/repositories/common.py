import abc

import sqlalchemy.ext.asyncio as async_alchemy


class SQLAlchemyRepo:
    def __init__(self, session: async_alchemy.AsyncSession):
        self._session = session

    @property
    def session(self) -> async_alchemy.AsyncSession:
        return self._session


class AbstractUnitOfWork(abc.ABC):
    @abc.abstractmethod
    async def __aenter__(self): ...

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abc.abstractmethod
    async def commit(self): ...

    @abc.abstractmethod
    async def rollback(self): ...
