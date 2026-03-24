from fastapi import APIRouter
from fastapi_cache.decorator import cache
from src.tasks.tasks import task_test


from src.schemas.facilities import FacilitiesAddSchema
from src.api.dependencies import DBDep


router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('/')
@cache(expire=10)
async def get_facilities(
        db: DBDep,
):
    return await db.facilitiesModel.get_filtered_objects()


@router.post('/')
async def post_facilities(
        db: DBDep,
        data: FacilitiesAddSchema
):

    facilities = await db.facilitiesModel.add_obj(data)

    task_test.delay()

    await db.save()
    return facilities
