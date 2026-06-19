from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey, TIMESTAMP, false, DateTime, func, Enum as SAEnum
from datetime import datetime
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    CANCELED = "canceled"


class BookingsOrm(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    from_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    to_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    price: Mapped[int]
    status: Mapped[Status] = mapped_column(
        SAEnum(Status, native_enum=False, length=20),
        default=Status.PENDING.value,
        server_default=Status.PENDING.value
    )
    is_paid: Mapped[bool] = mapped_column(default=False, server_default=false())
    paid_date: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.timezone('Asia/Bishkek', func.now()))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone('Asia/Bishkek', func.now()),
        onupdate=func.timezone('Asia/Bishkek', func.now())
    )

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.to_date - self.from_date).days
