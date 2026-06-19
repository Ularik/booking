from fastapi.params import Query
from datetime import date
from src.api.dependencies import DBDep, AuthUserDep, PaginationDep
from fastapi import APIRouter, Body, HTTPException
from src.exceptions import ObjectNotFoundException, NotEmptyRoomsException
from src.schemas.bookings import BookingAddRequestSchema
from src.services.bookings import BookingServices
from src.tasks.tasks import task_generate_pdf, get_todays_bookings
from celery import chain

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/me")
async def get_my_bookings(
    user_id: AuthUserDep,
    db: DBDep,
    paging: PaginationDep,
):
    return await BookingServices(db).get_my_bookings(user_id, limit=paging.limit, offset=paging.offset)


@router.get("/")
async def get_all_bookings(db: DBDep, paging: PaginationDep):
    return BookingServices(db).get_all_bookings(limit=paging.limit, offset=paging.offset)


@router.post("/")
async def post_bookings(
    user_id: AuthUserDep,
    db: DBDep,
    data: BookingAddRequestSchema = Body(
        openapi_examples={
            "1": {
                "summary": "",
                "description": "",
                "value": {
                    "room_id": 17,
                    "from_date": "2026-03-18",
                    "to_date": "2026-03-20",
                },
            }
        }
    ),
):
    try:
        new_booking = await BookingServices(db).add_booking(user_id, data)
    except ObjectNotFoundException:
        raise HTTPException(400, "Такой квартиры нет")
    except NotEmptyRoomsException as ex:
        raise HTTPException(409, ex.detail)
    return new_booking


@router.delete("/")
async def delete_bookings(
    user_id: AuthUserDep,
    db: DBDep,
    room_id: int,
    from_date: date = Query(date(2026, 3, 17)),
    to_date: date = Query(date(2026, 3, 23)),
):
    await BookingServices(db).delete_booking(room_id, from_date, to_date)
    return {"message": "delete success"}


@router.post("/reports/generate/")
async def start_report_generation(request):
    report_workflow = chain(
        get_todays_bookings.s() | task_generate_pdf.s()
    )

    result_group = report_workflow.delay()

    return {"task_id": result_group.id, "status": "processing"}