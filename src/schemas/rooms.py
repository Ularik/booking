from pydantic import BaseModel, ConfigDict
from src.schemas.facilities import FacilitiesSchema


class RoomSchema(BaseModel):
    id: int
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int

    model_config = ConfigDict(from_attributes=True, extra='ignore')


class RoomRelSchema(RoomSchema):
    facilities: list["FacilitiesSchema"]


class RoomAddRequestSchema(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int
    facilities: list[int] | None


class RoomAddSchema(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int


class RoomEditRequestSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities: list[int] | None


class RoomEditSchema(BaseModel):
    hotel_id: int | None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
