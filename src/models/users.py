from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime, func
from src.database import Base
from datetime import datetime
from enum import Enum


class UserStatus(Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    USER = "USER"


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    nik_name: Mapped[str | None] = mapped_column(String(50))
    hashed_password: Mapped[bytes]
    status: Mapped[UserStatus] = mapped_column(default=UserStatus.USER, server_default=UserStatus.USER.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.timezone('Asia/Bishkek', func.now()))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone('Asia/Bishkek', func.now()),
        onupdate=func.timezone('Asia/Bishkek', func.now())
    )