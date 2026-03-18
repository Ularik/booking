from fastapi import APIRouter, Body
from src.schemas.facilities import FacilitiesSchema, FacilitiesAddSchema
from fastapi import Query
from datetime import date
from src.api.dependencies import PaginationDep
from src.api.dependencies import DBDep


router = APIRouter(prefix='/facilities', tags=['Удобства'])


@router.get('/')
async def get_facilities(
        db: DBDep,
        paging: PaginationDep,
):
    facilities = await db.facilitiesModel.get_filtered_objects(limit=paging.limit, offset=paging.offset)
    return facilities


@router.post('/')
async def post_facilities(
        db: DBDep,
        data: FacilitiesAddSchema
):

    facilities = await db.facilitiesModel.add_obj(data)
    await db.save()
    return facilities
