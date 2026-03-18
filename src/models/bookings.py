from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey, TIMESTAMP
from datetime import datetime


class BookingsOrm(Base):
    __tablename__ = 'bookings'
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    from_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    to_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    price: Mapped[int]

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.to_date - self.from_date).days