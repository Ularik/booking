from fastapi import APIRouter, Body, Query, HTTPException
from fastapi_cache.decorator import cache
from datetime import date

from src.exception_handlers.exceptions import NotValidTimedeltaException, ObjectNotFoundException, UniqueObjIsExistException
from src.schemas.hotels import HotelSchema, HotelOutSchema, HotelsEditSchema
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelsServices

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.post("/", response_model=HotelOutSchema)
async def add_hotel(
    db: DBDep,
    data: HotelSchema = Body(
        openapi_examples={
            "1": {
                "summary": "base example",
                "description": "base example",
                "value": {"title": "Garden", "location": "Bishkek"},
            }
        }
    ),
):
    try:
        new_hotel = await HotelsServices(db).add_hotel(data)
    except UniqueObjIsExistException as err:
        raise HTTPException(status_code=404, detail=err.detail)
    await db.save()
    return new_hotel


@router.get("/hotels_with_free_rooms")
@cache(expire=15)
async def get_empty_hotels(
    db: DBDep,
    paging: PaginationDep,
    title: str = Query(None, description="Название"),
    location: str = Query(None, description="Локация"),
    from_date: date = Query(date(2026, 3, 17)),
    to_date: date = Query(date(2026, 3, 23)),
) -> list[HotelOutSchema]:
    try:
        hotels = await HotelsServices(db).get_empty_hotels(
            from_date, to_date, title=title, location=location, limit=paging.limit, offset=paging.offset
        )
    except NotValidTimedeltaException as err:
        raise HTTPException(400, detail=err.detail)

    return hotels


@router.get("/{hotel_id}")
@cache(expire=10)
async def get_one_hotel(db: DBDep, hotel_id: int):
    try:
        res = await HotelsServices(db).get_one_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException as err:
        raise HTTPException(400, detail=err.detail)
    return res


@router.patch("/{hotel_id}")
async def patch_hotel(db: DBDep, data: HotelsEditSchema, hotel_id: int):
    try:
        res = await HotelsServices(db).path_hotel(data=data, hotel_id=hotel_id)
    except ObjectNotFoundException as err:
        raise HTTPException(status_code=404, detail=err.detail)
    await db.save()
    return res


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, id: int):
    try:
        await HotelsServices(db).delete_hotel(hotel_id=id)
    except ObjectNotFoundException as err:
        raise HTTPException(status_code=404, detail=err.detail)
    await db.save()

    return {200: "delete"}
