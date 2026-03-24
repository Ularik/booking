from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class FacilitiesOrm(Base):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    rooms: Mapped[list["RoomsOrm"]] = relationship(
        secondary='rooms_facilities',
        back_populates='facilities'
    )


class RoomsFacilitiesOrm(Base):
    __tablename__ = 'rooms_facilities'
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id', ondelete="CASCADE"))
    facility_id: Mapped[int] = mapped_column(ForeignKey('facilities.id', ondelete="CASCADE"))
