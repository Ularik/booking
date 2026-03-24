from src.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import NullPool


engine = create_async_engine(settings.DB_URL, echo=False)
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

AsyncSession = async_sessionmaker(engine, expire_on_commit=False)
AsyncSessionNullPool = async_sessionmaker(engine_null_pool, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
