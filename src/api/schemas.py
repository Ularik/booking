from pydantic import BaseModel, ConfigDict
from typing import Optional


class HotelOutSchema(BaseModel):
    id: int
    title: str
    location: str
    model_config = ConfigDict(from_attributes=True, extra='ignore')


class HotelSchema(BaseModel):
    title: str
    location: str

    model_config = ConfigDict(from_attributes=True, extra='ignore')