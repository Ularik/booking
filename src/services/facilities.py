from src.exception_handlers.exceptions import UniqueObjIsExistException, RoomNotFoundException, ObjectNotFoundException, \
    FacilityIsExistException, FacilityNotFoundException
from src.services.base import BaseService
from src.schemas.facilities import FacilitiesAddSchema, FacilitiesSchema

class FacilitiesService(BaseService):

    async def get_facilities(self, **filters) -> list[FacilitiesSchema]:
        return await self.db.facilitiesModel.get_filtered_objects(**filters)

    async def post_facilities(self, data: FacilitiesAddSchema) -> FacilitiesSchema:
        try:
            result = await self.db.facilitiesModel.add_obj(data)
            await self.db.save()
            return result
        except UniqueObjIsExistException as err:
            raise FacilityIsExistException from err
        except ObjectNotFoundException as err:
            raise RoomNotFoundException from err

    async def delete_facility(self, facility_id: int) -> dict:
        try:
            await self.db.facilitiesModel.check_exist_delete(id=facility_id)
            await self.db.save()
            return {200: 'Удобство удалено'}
        except ObjectNotFoundException as err:
            raise FacilityNotFoundException from err