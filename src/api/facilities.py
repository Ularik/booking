from fastapi import APIRouter
from fastapi_cache.decorator import cache
from src.schemas.facilities import FacilitiesAddSchema
from src.services.facilities import FacilitiesService
from src.api.dependencies import DBDep, AuthUserDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/")
@cache(expire=10)
async def get_facilities(
    db: DBDep,
):
    return await FacilitiesService(db).get_facilities()


@router.post("/")
async def post_facilities(db: DBDep, data: FacilitiesAddSchema):

    facilities = await FacilitiesService(db).post_facilities(data)
    return facilities


@router.delete("/{facility_id}")
async def delete_facility(
        user_id: AuthUserDep,
        db: DBDep,
        facility_id: int
):
    return await FacilitiesService(db).delete_facility(facility_id=facility_id)