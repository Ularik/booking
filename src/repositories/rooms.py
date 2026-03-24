from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import RoomRelSchema
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.repositories.utils import get_free_rooms_ids
from src.repositories.mappers.mappers import RoomMapper, RoomRelMapper


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomMapper

    async def get_free_rooms(
            self,
            from_date: date,
            to_date: date,
            hotel_id: int = None,
            limit: int = 10,
            offset: int = 0) -> list[RoomRelSchema]:

        free_rooms_ids = await get_free_rooms_ids(from_date=from_date, to_date=to_date, hotel_id=hotel_id)
        #  rooms_list = await self.get_filtered_objects(RoomsOrm.id.in_(free_rooms_ids), limit=limit, offset=offset)
        query = (
            select(self.model)
            .options(
                joinedload(self.model.facilities)
            )
            .filter(RoomsOrm.id.in_(free_rooms_ids))
        )
        results = await self.session.execute(query)
        return [RoomRelMapper.map_to_domain_entity(r) for r in results.scalars().unique()]

    async def get_one_room(self, room_id: int, hotel_id: int) -> RoomRelSchema:
        query = (
            select(self.model)
            .options(
                joinedload(self.model.facilities)
            )
            .filter(RoomsOrm.id == room_id)
        )
        results = await self.session.execute(query)
        room = results.scalars().first()
        return RoomRelMapper.map_to_domain_entity(room)
