import typing

import sqlalchemy.ext.asyncio as async_alchemy
import sqlalchemy.orm as orm_alchemy

import src.config as config


class SessionManager:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.refresh()

    def get_session_maker(self) -> orm_alchemy.sessionmaker:
        return orm_alchemy.sessionmaker(
            self.engine,
            class_=async_alchemy.AsyncSession,
            expire_on_commit=False,
        )

    def refresh(self) -> None:
        self.engine = async_alchemy.create_async_engine(
            config.get_db_url(),
            future=True,
            echo=True,
        )


async def get_db() -> typing.AsyncGenerator[async_alchemy.AsyncSession, None]:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session
