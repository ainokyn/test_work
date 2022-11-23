from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


class User(SQLAlchemyBaseUserTable[int], Base):
    name = Column(String(100), nullable=False)
    surname = Column(String(150), nullable=False)
    patronymic = Column(String(100), nullable=False)
    balance = Column(Integer, nullable=False)


class Operation(Base):
    user_from = Column(Integer, ForeignKey("user.id"))
    amount = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    surname = Column(String(150), nullable=False)
    patronymic = Column(String(100), nullable=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
    commit = Column(Boolean, default=False)
