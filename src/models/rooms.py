import typing
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import ForeignKey, String, DateTime, func, select
from datetime import datetime

from src.models.bookings import BookingsOrm

if typing.TYPE_CHECKING:
    from src.models.facilities import FacilitiesOrm


class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(100))
    price: Mapped[int]
    quantity: Mapped[int]
    booked_count: Mapped[int] = column_property(
        select(func.count(BookingsOrm.id))
        .where(BookingsOrm.room_id == id, BookingsOrm.status == 'SUCCESS')
        .correlate_except(BookingsOrm)
        .scalar_subquery()
    )
    facilities: Mapped[list["FacilitiesOrm"]] = relationship(
        secondary="rooms_facilities", back_populates="rooms"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.timezone('Asia/Bishkek', func.now()))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone('Asia/Bishkek', func.now()),
        onupdate=func.timezone('Asia/Bishkek', func.now())
    )
