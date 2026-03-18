from pydantic import BaseModel, ConfigDict
from datetime import datetime


class BookingOutSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    from_date: datetime
    to_date: datetime
    price: int
    model_config = ConfigDict(from_attributes=True)


class BookingAddRequestSchema(BaseModel):
    room_id: int
    from_date: datetime
    to_date: datetime
    model_config = ConfigDict(from_attributes=True)


class BookingAddSchema(BaseModel):
    room_id: int
    user_id: int
    from_date: datetime
    to_date: datetime
    price: int
    model_config = ConfigDict(from_attributes=True)