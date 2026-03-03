from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from src.database import Base
from sqlalchemy import String


class HotelsOrm(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]


class RoomsOrm(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(100))
    price: Mapped[int]
    quantity: Mapped[int]