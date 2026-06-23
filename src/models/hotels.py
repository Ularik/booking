from sqlalchemy.orm import Mapped, mapped_column, validates
from src.database import Base
from sqlalchemy import String, DateTime, func, CheckConstraint, UniqueConstraint
from datetime import datetime


class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.timezone('Asia/Bishkek', func.now()))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone('Asia/Bishkek', func.now()),
        onupdate=func.timezone('Asia/Bishkek', func.now())
    )
    __table_args__ = (
        UniqueConstraint('title', 'location', name='_title_location_uc'),
    )

    @validates('title', 'location')
    def lowerCase(self, key, value):
        def lowercase_fields(self, key, value):
            if value is not None:
                return value.strip().lower()
            return value


