from fastapi import APIRouter, Body, Query
from src.schemas.hotels import HotelSchema, HotelOutSchema, HotelsEditSchema
from src.database import AsyncSession
from src.api.dependencies import PaginationDep
from src.repositories.hotels import HotelsRepository
from src.api.dependencies import DBDep
from datetime import date

router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.post("/", response_model=HotelOutSchema)
async def add_hotel(
        db: DBDep,
        data: HotelSchema = Body(openapi_examples={
    "1": {
        "summary": "base example",
        "description": "base example",
        "value": {
            "title": "Garden",
            "location": "Bishkek"
        }
    }
})):
    new_hotel = await db.hotelsModel.add_obj(data)
    await db.save()
    return new_hotel


@router.get("/empty_hotels")
async def get_empty_hotels(
        db: DBDep,
        paging: PaginationDep,
        title: str = Query(None, description="Название"),
        location: str = Query(None, description="Локация"),
        from_date: date = Query(date(2026, 3, 17)),
        to_date: date = Query(date(2026, 3, 23))
):
    hotels = await db.hotelsModel.get_hotels_with_free_rooms(
        from_date,
        to_date,
        title=title,
        location=location,
        limit=paging.limit,
        offset=paging.offset)

    return hotels


@router.get("/{hotel_id}")
async def get_one_hotel(
        db: DBDep,
        hotel_id: int):
    res = await db.hotelsModel.get_one_or_none(id=hotel_id)
    return res


@router.patch('/{hotel_id}')
async def patch_hotel(
        db: DBDep,
        data: HotelsEditSchema,
        hotel_id: int):

    res = await db.hotelsModel.edit(
        data=data,
        id=hotel_id,
        exclude_unset=True
    )
    await db.save()
    return res


@router.delete("/{hotel_id}")
async def delete_hotel(
        db: DBDep,
        id: int):
    await db.hotelsModel.delete(id=id)
    await db.save()

    return {200: "delete"}
