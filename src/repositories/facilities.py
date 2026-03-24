from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm
from src.repositories.mappers.mappers import FacilityMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityMapper
