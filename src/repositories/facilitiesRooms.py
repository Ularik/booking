from src.repositories.base import BaseRepository
from src.models.facilities import RoomsFacilities
from src.schemas.facilities import FacilitiesRoomsSchema, FacilitiesRoomsAddSchema
from sqlalchemy import select, update, insert

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilities
    schema = FacilitiesRoomsSchema

    async def set_rooms_facilities(self, room_id, facilities: list[int] = None, **kwargs):

        results = await self.get_filtered_objects(room_id=room_id)
        old_facilities = [r.facility_id for r in results]

        inserted_facilities = list(set(facilities) - set(old_facilities))
        deleted_facilities = list(set(old_facilities) - set(facilities))

        if deleted_facilities:
            facilities_filter = self.model.facility_id.in_(deleted_facilities)
            await self.delete_bulk(facilities_filter, room_id=room_id)

        if inserted_facilities:
            inserted_facilities = [FacilitiesRoomsAddSchema(room_id=room_id, facility_id=f) for f in inserted_facilities]
            await self.add_bulk(inserted_facilities)
