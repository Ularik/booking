from pydantic import BaseModel, ConfigDict
from datetime import datetime
from src.models.bookings import Status


class BookingOutSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    from_date: datetime
    to_date: datetime
    price: int
    status: Status
    is_paid: bool
    paid_date: datetime | None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class BookingAddRequestSchema(BaseModel):
    room_id: int
    from_date: datetime
    to_date: datetime
    model_config = ConfigDict(from_attributes=True)


class BookingAddSchema(BaseModel):
    room_id: int
    user_id: int
    price: int | None = None
    from_date: datetime
    to_date: datetime
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class BookingUpdateRequestSchema(BaseModel):
    room_id: int
    from_date: datetime
    to_date: datetime


class BookingUpdateSchema(BaseModel):
    room_id: int
    price: int
    status: Status
    from_date: datetime
    to_date: datetime


class BookingUpdateByCelerySchema(BaseModel):
    room_id: int | None = None
    status: Status
    from_date: datetime | None = None
    to_date: datetime | None = None

