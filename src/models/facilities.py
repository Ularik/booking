import typing
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey, DateTime, func
from datetime import datetime

if typing.TYPE_CHECKING:
    from src.models.rooms import RoomsOrm


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    rooms: Mapped[list["RoomsOrm"]] = relationship(
        secondary="rooms_facilities", back_populates="facilities"
    )

    @validates('title')
    def title_lower(self, key, title: str):
        if not title.islower():
            title = title.lower()
        return title

class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.timezone('Asia/Bishkek', func.now()))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone('Asia/Bishkek', func.now()),
        onupdate=func.timezone('Asia/Bishkek', func.now())
    )
