from pydantic import BaseModel, ConfigDict, Field


class HotelsEditSchema(BaseModel):
    title: str = Field(None)
    location: str = Field(None)


class HotelSchema(BaseModel):
    title: str
    location: str

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class HotelOutSchema(HotelSchema):
    id: int
