from src.models.hotels import HotelsOrm
from sqlalchemy import insert, select, func
from fastapi import APIRouter, Body, Query
from src.api.schemas import HotelSchema, HotelOutSchema
from src.database import AsyncSession
from src.api.dependencies import PaginationDep
from src.repositories.hotels import HotelsRepository


router = APIRouter()


@router.post("/hotels", response_model=HotelOutSchema)
async def add_hotel(data: HotelSchema = Body(openapi_examples={
    "1": {
        "summary": "base example",
        "description": "base example",
        "value": {
            "title": "Garden",
            "location": "Bishkek"
        }
    }
})):
    async with AsyncSession() as session:
        new_hotel = await HotelsRepository(session).add_obj(data)
        await session.commit()

        return new_hotel


@router.get("/hotels")
async def get_hotels(
        paging: PaginationDep,
        title: str = Query(None, description="Название"),
        location: str = Query(None, description="Локация")
):
    async with AsyncSession() as session:
        hotels = await HotelsRepository(session).get_objects(
         title=title,
         location=location,
         limit=paging.limit,
         offset=paging.offset
         )

    return hotels


@router.put('/hotels/{hotel_id}')
async def put_hotel(data: HotelSchema, hotel_id: int):
    async with AsyncSession() as session:
        try:

            res = await HotelsRepository(session).edit(
                data=data,
                id=hotel_id
            )
        except BaseException:
            return {404: 'not exist'}

        await session.commit()
        return res


@router.delete("/hotels/{hotel_id}")
async def delete_hotel(id: int):
    async with AsyncSession() as session:
        try:
            res = await HotelsRepository(session).delete(id=id)
        except BaseException:
            return {404: 'not exist'}

    await session.commit()
    return res
