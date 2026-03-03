from src.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(settings.DB_URL, echo=False)

AsyncSession = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
