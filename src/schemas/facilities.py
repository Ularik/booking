from pydantic import BaseModel, ConfigDict


class FacilitiesSchema(BaseModel):
    id: int
    title: str
    model_config = ConfigDict(from_attributes=True)


class FacilitiesAddSchema(BaseModel):
    title: str


class FacilitiesRoomsAddSchema(BaseModel):
    room_id: int
    facility_id: int


class FacilitiesRoomsSchema(FacilitiesRoomsAddSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)