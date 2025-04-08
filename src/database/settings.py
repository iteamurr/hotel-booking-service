import sqlalchemy.ext.asyncio as async_alchemy
import sqlalchemy.orm as orm_alchemy

import src.config as config


engine = async_alchemy.create_async_engine(
    config.get_db_url(),
    future=True,
    echo=True,
)

async_session = orm_alchemy.sessionmaker(
    engine,
    expire_on_commit=False,
    class_=async_alchemy.AsyncSession,
)
