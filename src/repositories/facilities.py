from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm
from src.schemas.facilities import FacilitiesSchema


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = FacilitiesSchema
